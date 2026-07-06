from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.auth import can_manage_desag_content, can_manage_official_content, get_current_user
from app.database import get_db
from app.models import Announcement, NoticeType, ScopeType, User
from app.schemas import AnnouncementCreate, AnnouncementOut

router = APIRouter(prefix='/api/announcements', tags=['announcements'])


def _base_visible_query(db: Session, user: User):
    query = db.query(Announcement).filter(Announcement.status == 'PUBLISHED')
    filters = [Announcement.scope_type.in_([ScopeType.ALL.value, ScopeType.NATIONAL.value])]
    if user.region:
        filters.append(Announcement.region == user.region)
    if user.center_id:
        filters.append(Announcement.center_id == user.center_id)
    if user.programme:
        filters.append(Announcement.programme == user.programme)
    if user.level:
        filters.append(Announcement.level == user.level)
    return query.filter(or_(*filters))


@router.get('', response_model=list[AnnouncementOut])
def list_announcements(
    notice_type: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = _base_visible_query(db, current_user)
    if notice_type:
        query = query.filter(Announcement.notice_type == notice_type)
    return query.order_by(Announcement.is_pinned.desc(), Announcement.created_at.desc()).limit(100).all()


@router.post('', response_model=AnnouncementOut)
def create_announcement(
    payload: AnnouncementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if payload.notice_type == NoticeType.DESAG.value:
        if not can_manage_desag_content(current_user.role):
            raise HTTPException(status_code=403, detail='Only DESAG-approved roles can create DESAG notices')
        if current_user.role == 'DESAG_REGIONAL' and payload.region and payload.region != current_user.region:
            raise HTTPException(status_code=403, detail='Regional DESAG users can only post within their region')
        if current_user.role == 'DESAG_CENTER' and payload.center_id and payload.center_id != current_user.center_id:
            raise HTTPException(status_code=403, detail='Centre DESAG users can only post within their centre')
    elif payload.notice_type == NoticeType.OFFICIAL_CODE.value:
        if not can_manage_official_content(current_user.role):
            raise HTTPException(status_code=403, detail='Only approved CoDE roles can create official notices')
    else:
        raise HTTPException(status_code=400, detail='Unsupported notice type')

    notice = Announcement(**payload.model_dump(), created_by_id=current_user.id)
    db.add(notice)
    db.commit()
    db.refresh(notice)
    return notice
