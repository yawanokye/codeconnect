from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.auth import can_manage_desag_content, can_manage_official_content, get_current_user
from app.database import get_db
from app.models import Event, EventType, User
from app.schemas import EventCreate, EventOut

router = APIRouter(prefix='/api/events', tags=['events'])


@router.get('', response_model=list[EventOut])
def list_events(
    event_type: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Event)
    filters = []
    if current_user.region:
        filters.append(Event.region == current_user.region)
    if current_user.center_id:
        filters.append(Event.center_id == current_user.center_id)
    if current_user.programme:
        filters.append(Event.programme == current_user.programme)
    if current_user.level:
        filters.append(Event.level == current_user.level)
    filters.append(Event.region.is_(None))
    filters.append(Event.center_id.is_(None))
    query = query.filter(or_(*filters))
    if event_type:
        query = query.filter(Event.event_type == event_type)
    return query.order_by(Event.start_at.asc()).limit(100).all()


@router.post('', response_model=EventOut)
def create_event(payload: EventCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if payload.event_type == EventType.DESAG.value:
        if not can_manage_desag_content(current_user.role):
            raise HTTPException(status_code=403, detail='Only DESAG-approved roles can create DESAG events')
    else:
        if not can_manage_official_content(current_user.role):
            raise HTTPException(status_code=403, detail='Only approved CoDE roles can create academic or official events')
    event = Event(**payload.model_dump(), created_by_id=current_user.id)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
