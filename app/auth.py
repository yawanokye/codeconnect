from datetime import datetime, timedelta, timezone
from typing import Iterable
import base64
import hashlib
import hmac
import secrets

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.models import User

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/login')

PASSWORD_ITERATIONS = 210_000


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, PASSWORD_ITERATIONS)
    return 'pbkdf2_sha256${}${}'.format(
        base64.b64encode(salt).decode('ascii'),
        base64.b64encode(digest).decode('ascii'),
    )


def verify_password(password: str, password_hash: str) -> bool:
    try:
        algorithm, salt_b64, digest_b64 = password_hash.split('$', 2)
        if algorithm != 'pbkdf2_sha256':
            return False
        salt = base64.b64decode(salt_b64)
        expected = base64.b64decode(digest_b64)
        actual = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, PASSWORD_ITERATIONS)
        return hmac.compare_digest(actual, expected)
    except Exception:
        return False


def create_access_token(subject: str) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {'sub': subject, 'exp': expires}
    return jwt.encode(payload, settings.secret_key, algorithm='HS256')


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=['HS256'])
        user_id = payload.get('sub')
        if user_id is None:
            raise credentials_error
    except jwt.PyJWTError as exc:
        raise credentials_error from exc

    user = db.get(User, int(user_id))
    if not user or not user.is_active:
        raise credentials_error
    return user


def require_roles(allowed_roles: Iterable[str]):
    allowed_set = set(allowed_roles)

    def checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_set:
            raise HTTPException(status_code=403, detail='You do not have permission to perform this action')
        return current_user

    return checker


def can_manage_official_content(role: str) -> bool:
    return role in {'SUPER_ADMIN', 'CODE_ADMIN', 'MANAGEMENT', 'PROVOST', 'COLLEGE_REGISTRAR', 'DIRECTOR', 'CAMPUS_DIRECTOR', 'HEAD_OF_DEPARTMENT', 'DEPARTMENTAL_REGISTRATION_OFFICER', 'UNIT_COORDINATOR', 'SECTION_HEAD', 'FINANCE_OFFICER', 'PROCUREMENT_HEAD', 'ADMISSIONS_HEAD', 'EXAMS_HEAD', 'REGIONAL_COORDINATOR', 'CENTER_COORDINATOR', 'STUDENT_SUPPORT', 'QA_OFFICER'}


def can_manage_desag_content(role: str) -> bool:
    return role in {'SUPER_ADMIN', 'CODE_ADMIN', 'DESAG_NATIONAL', 'DESAG_REGIONAL', 'DESAG_CENTER'}


def can_manage_tickets(role: str) -> bool:
    return role in {'SUPER_ADMIN', 'CODE_ADMIN', 'MANAGEMENT', 'PROVOST', 'COLLEGE_REGISTRAR', 'DIRECTOR', 'CAMPUS_DIRECTOR', 'HEAD_OF_DEPARTMENT', 'DEPARTMENTAL_REGISTRATION_OFFICER', 'UNIT_COORDINATOR', 'SECTION_HEAD', 'FINANCE_OFFICER', 'PROCUREMENT_HEAD', 'ADMISSIONS_HEAD', 'EXAMS_HEAD', 'REGIONAL_COORDINATOR', 'CENTER_COORDINATOR', 'STUDENT_SUPPORT', 'QA_OFFICER', 'DESAG_NATIONAL', 'DESAG_REGIONAL', 'DESAG_CENTER'}
