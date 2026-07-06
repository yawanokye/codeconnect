from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    user: 'UserOut'


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: str
    region: Optional[str] = None
    programme: Optional[str] = None
    level: Optional[str] = None
    center_id: Optional[int] = None
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class StudyCentreBase(BaseModel):
    name: str
    region: str
    zone: Optional[str] = None
    town: Optional[str] = None
    coordinator_name: Optional[str] = None
    coordinator_phone: Optional[str] = None
    is_active: bool = True


class StudyCentreCreate(StudyCentreBase):
    pass


class StudyCentreOut(StudyCentreBase):
    id: int

    class Config:
        from_attributes = True


class AnnouncementCreate(BaseModel):
    title: str
    body: str
    notice_type: str = 'OFFICIAL_CODE'
    scope_type: str = 'ALL'
    region: Optional[str] = None
    programme: Optional[str] = None
    level: Optional[str] = None
    center_id: Optional[int] = None
    is_pinned: bool = False


class AnnouncementOut(AnnouncementCreate):
    id: int
    status: str
    created_by_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TicketCreate(BaseModel):
    subject: str
    category: str
    description: str
    priority: str = 'NORMAL'
    region: Optional[str] = None
    center_id: Optional[int] = None


class TicketUpdate(BaseModel):
    status: Optional[str] = None
    assigned_to_id: Optional[int] = None
    priority: Optional[str] = None


class TicketOut(BaseModel):
    id: int
    reference: str
    subject: str
    category: str
    description: str
    status: str
    priority: str
    student_id: int
    assigned_to_id: Optional[int] = None
    region: Optional[str] = None
    center_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    event_type: str = 'CODE'
    start_at: datetime
    end_at: Optional[datetime] = None
    region: Optional[str] = None
    programme: Optional[str] = None
    level: Optional[str] = None
    center_id: Optional[int] = None


class EventOut(EventCreate):
    id: int
    created_by_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class DiscussionChannelCreate(BaseModel):
    name: str
    description: Optional[str] = None
    channel_type: str = 'COURSE'
    region: Optional[str] = None
    programme: Optional[str] = None
    level: Optional[str] = None
    center_id: Optional[int] = None
    is_moderated: bool = True


class DiscussionChannelOut(DiscussionChannelCreate):
    id: int
    created_by_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class DiscussionMessageCreate(BaseModel):
    body: str


class DiscussionMessageOut(BaseModel):
    id: int
    channel_id: int
    body: str
    author_id: int
    is_hidden: bool
    created_at: datetime

    class Config:
        from_attributes = True


class AdministrativeOfficeOut(BaseModel):
    id: int
    name: str
    office_type: str
    dashboard_role: str
    lead_title: Optional[str] = None
    lead_name: Optional[str] = None
    scope: Optional[str] = None
    reporting_line: Optional[str] = None
    key_modules: str
    can_publish_official: bool
    can_handle_tickets: bool
    can_view_analytics: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class DashboardOut(BaseModel):
    users: int
    centres: int
    administrative_offices: int
    announcements: int
    desag_announcements: int
    open_tickets: int
    events: int
    discussion_channels: int


class LinkHubOut(BaseModel):
    myucc_url: str
    ucc_elearning_url: str
    code_website_url: str
