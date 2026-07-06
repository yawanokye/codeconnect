from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.auth import can_manage_tickets, get_current_user
from app.database import get_db
from app.models import Ticket, User
from app.schemas import TicketCreate, TicketOut, TicketUpdate

router = APIRouter(prefix='/api/tickets', tags=['tickets'])


def make_reference(db: Session) -> str:
    count = db.query(Ticket).count() + 1
    return f'CODE-{datetime.utcnow().strftime("%Y%m%d")}-{count:05d}'


@router.get('', response_model=list[TicketOut])
def list_tickets(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Ticket)
    if not can_manage_tickets(current_user.role):
        query = query.filter(Ticket.student_id == current_user.id)
    elif current_user.role in {'REGIONAL_COORDINATOR', 'DESAG_REGIONAL'} and current_user.region:
        query = query.filter(or_(Ticket.region == current_user.region, Ticket.region.is_(None)))
    elif current_user.role in {'CENTER_COORDINATOR', 'DESAG_CENTER'} and current_user.center_id:
        query = query.filter(or_(Ticket.center_id == current_user.center_id, Ticket.center_id.is_(None)))
    return query.order_by(Ticket.created_at.desc()).limit(100).all()


@router.post('', response_model=TicketOut)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ticket = Ticket(
        reference=make_reference(db),
        subject=payload.subject,
        category=payload.category,
        description=payload.description,
        priority=payload.priority,
        student_id=current_user.id,
        region=payload.region or current_user.region,
        center_id=payload.center_id or current_user.center_id,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


@router.patch('/{ticket_id}', response_model=TicketOut)
def update_ticket(
    ticket_id: int,
    payload: TicketUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not can_manage_tickets(current_user.role):
        raise HTTPException(status_code=403, detail='You do not have permission to update tickets')
    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail='Ticket not found')
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(ticket, field, value)
    db.commit()
    db.refresh(ticket)
    return ticket
