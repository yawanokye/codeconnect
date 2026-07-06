from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.config import get_settings
from app.database import get_db
from app.models import AdministrativeOffice, Announcement, DiscussionChannel, Event, NoticeType, StudyCentre, Ticket, TicketStatus, User
from app.schemas import DashboardOut, LinkHubOut

router = APIRouter(prefix='/api', tags=['dashboard'])


@router.get('/dashboard', response_model=DashboardOut)
def dashboard(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return DashboardOut(
        users=db.query(User).count(),
        centres=db.query(StudyCentre).count(),
        administrative_offices=db.query(AdministrativeOffice).filter(AdministrativeOffice.is_active.is_(True)).count(),
        announcements=db.query(Announcement).filter(Announcement.notice_type == NoticeType.OFFICIAL_CODE.value).count(),
        desag_announcements=db.query(Announcement).filter(Announcement.notice_type == NoticeType.DESAG.value).count(),
        open_tickets=db.query(Ticket).filter(Ticket.status != TicketStatus.CLOSED.value).count(),
        events=db.query(Event).count(),
        discussion_channels=db.query(DiscussionChannel).count(),
    )


@router.get('/links', response_model=LinkHubOut)
def link_hub(_: User = Depends(get_current_user)):
    settings = get_settings()
    return LinkHubOut(
        myucc_url=settings.myucc_url,
        ucc_elearning_url=settings.ucc_elearning_url,
        code_website_url=settings.code_website_url,
    )
