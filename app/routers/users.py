from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import hash_password, require_roles
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserOut

router = APIRouter(prefix='/api/users', tags=['users'])
ADMIN_ROLES = ['SUPER_ADMIN', 'CODE_ADMIN']


@router.get('', response_model=list[UserOut])
def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(ADMIN_ROLES)),
):
    return db.query(User).order_by(User.created_at.desc()).all()


@router.post('', response_model=UserOut)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(ADMIN_ROLES)),
):
    exists = db.query(User).filter(User.email == payload.email.lower()).first()
    if exists:
        raise HTTPException(status_code=400, detail='Email already exists')
    user = User(
        full_name=payload.full_name,
        email=payload.email.lower(),
        password_hash=hash_password(payload.password),
        role=payload.role,
        region=payload.region,
        programme=payload.programme,
        level=payload.level,
        center_id=payload.center_id,
        is_active=payload.is_active,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
