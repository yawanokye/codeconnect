from fastapi import APIRouter, Depends
from sqlalchemy import case
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import AdministrativeOffice, User
from app.schemas import AdministrativeOfficeOut

router = APIRouter(prefix='/api/admin-offices', tags=['administrative offices'])


@router.get('', response_model=list[AdministrativeOfficeOut])
def list_administrative_offices(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    office_order = case(
        (AdministrativeOffice.office_type == 'EXECUTIVE', 1),
        (AdministrativeOffice.office_type == 'DIRECTORATE', 2),
        (AdministrativeOffice.office_type == 'CAMPUS', 3),
        (AdministrativeOffice.office_type == 'DEPARTMENT', 4),
        (AdministrativeOffice.office_type == 'DEPARTMENTAL_REGISTRATION', 5),
        (AdministrativeOffice.office_type == 'UNIT', 6),
        (AdministrativeOffice.office_type == 'SECTION', 7),
        (AdministrativeOffice.office_type == 'FIELD_OPERATIONS', 8),
        else_=99,
    )
    return (
        db.query(AdministrativeOffice)
        .filter(AdministrativeOffice.is_active.is_(True))
        .order_by(office_order, AdministrativeOffice.name.asc())
        .all()
    )
