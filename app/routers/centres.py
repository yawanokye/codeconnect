from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import require_roles, get_current_user
from app.database import get_db
from app.models import StudyCentre, User
from app.schemas import StudyCentreCreate, StudyCentreOut

router = APIRouter(prefix='/api/centres', tags=['centres'])
MANAGER_ROLES = ['SUPER_ADMIN', 'CODE_ADMIN', 'MANAGEMENT', 'REGIONAL_COORDINATOR']


@router.get('', response_model=list[StudyCentreOut])
def list_centres(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(StudyCentre).filter(StudyCentre.is_active == True).order_by(StudyCentre.region, StudyCentre.name).all()


@router.post('', response_model=StudyCentreOut)
def create_centre(
    payload: StudyCentreCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(MANAGER_ROLES)),
):
    exists = db.query(StudyCentre).filter(StudyCentre.name == payload.name).first()
    if exists:
        raise HTTPException(status_code=400, detail='Study centre already exists')
    centre = StudyCentre(**payload.model_dump())
    db.add(centre)
    db.commit()
    db.refresh(centre)
    return centre
