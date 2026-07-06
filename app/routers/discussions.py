from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import DiscussionChannel, DiscussionMessage, User
from app.schemas import DiscussionChannelCreate, DiscussionChannelOut, DiscussionMessageCreate, DiscussionMessageOut

router = APIRouter(prefix='/api/discussions', tags=['discussions'])


@router.get('/channels', response_model=list[DiscussionChannelOut])
def list_channels(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(DiscussionChannel)
    filters = [DiscussionChannel.region.is_(None), DiscussionChannel.center_id.is_(None)]
    if current_user.region:
        filters.append(DiscussionChannel.region == current_user.region)
    if current_user.center_id:
        filters.append(DiscussionChannel.center_id == current_user.center_id)
    if current_user.programme:
        filters.append(DiscussionChannel.programme == current_user.programme)
    if current_user.level:
        filters.append(DiscussionChannel.level == current_user.level)
    return query.filter(or_(*filters)).order_by(DiscussionChannel.created_at.desc()).limit(100).all()


@router.post('/channels', response_model=DiscussionChannelOut)
def create_channel(
    payload: DiscussionChannelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    allowed = {'SUPER_ADMIN', 'CODE_ADMIN', 'MANAGEMENT', 'REGIONAL_COORDINATOR', 'CENTER_COORDINATOR', 'TUTOR', 'DESAG_NATIONAL', 'DESAG_REGIONAL', 'DESAG_CENTER', 'CLASS_REP'}
    if current_user.role not in allowed:
        raise HTTPException(status_code=403, detail='You do not have permission to create discussion channels')
    channel = DiscussionChannel(**payload.model_dump(), created_by_id=current_user.id)
    db.add(channel)
    db.commit()
    db.refresh(channel)
    return channel


@router.get('/channels/{channel_id}/messages', response_model=list[DiscussionMessageOut])
def list_messages(channel_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    channel = db.get(DiscussionChannel, channel_id)
    if not channel:
        raise HTTPException(status_code=404, detail='Channel not found')
    return (
        db.query(DiscussionMessage)
        .filter(DiscussionMessage.channel_id == channel_id, DiscussionMessage.is_hidden == False)
        .order_by(DiscussionMessage.created_at.asc())
        .limit(200)
        .all()
    )


@router.post('/channels/{channel_id}/messages', response_model=DiscussionMessageOut)
def create_message(
    channel_id: int,
    payload: DiscussionMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    channel = db.get(DiscussionChannel, channel_id)
    if not channel:
        raise HTTPException(status_code=404, detail='Channel not found')
    message = DiscussionMessage(channel_id=channel_id, body=payload.body, author_id=current_user.id)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message
