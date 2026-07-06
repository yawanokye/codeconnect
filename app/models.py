from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Role(str, Enum):
    SUPER_ADMIN = 'SUPER_ADMIN'
    CODE_ADMIN = 'CODE_ADMIN'
    MANAGEMENT = 'MANAGEMENT'
    PROVOST = 'PROVOST'
    COLLEGE_REGISTRAR = 'COLLEGE_REGISTRAR'
    DIRECTOR = 'DIRECTOR'
    CAMPUS_DIRECTOR = 'CAMPUS_DIRECTOR'
    HEAD_OF_DEPARTMENT = 'HEAD_OF_DEPARTMENT'
    DEPARTMENTAL_REGISTRATION_OFFICER = 'DEPARTMENTAL_REGISTRATION_OFFICER'
    UNIT_COORDINATOR = 'UNIT_COORDINATOR'
    SECTION_HEAD = 'SECTION_HEAD'
    FINANCE_OFFICER = 'FINANCE_OFFICER'
    PROCUREMENT_HEAD = 'PROCUREMENT_HEAD'
    ADMISSIONS_HEAD = 'ADMISSIONS_HEAD'
    EXAMS_HEAD = 'EXAMS_HEAD'
    REGIONAL_COORDINATOR = 'REGIONAL_COORDINATOR'
    CENTER_COORDINATOR = 'CENTER_COORDINATOR'
    TUTOR = 'TUTOR'
    STUDENT_SUPPORT = 'STUDENT_SUPPORT'
    QA_OFFICER = 'QA_OFFICER'
    DESAG_NATIONAL = 'DESAG_NATIONAL'
    DESAG_REGIONAL = 'DESAG_REGIONAL'
    DESAG_CENTER = 'DESAG_CENTER'
    CLASS_REP = 'CLASS_REP'
    STUDENT = 'STUDENT'


class NoticeType(str, Enum):
    OFFICIAL_CODE = 'OFFICIAL_CODE'
    DESAG = 'DESAG'
    PEER = 'PEER'


class ScopeType(str, Enum):
    ALL = 'ALL'
    NATIONAL = 'NATIONAL'
    REGIONAL = 'REGIONAL'
    CENTER = 'CENTER'
    PROGRAMME = 'PROGRAMME'
    COURSE = 'COURSE'


class TicketStatus(str, Enum):
    OPEN = 'OPEN'
    ASSIGNED = 'ASSIGNED'
    IN_PROGRESS = 'IN_PROGRESS'
    RESOLVED = 'RESOLVED'
    CLOSED = 'CLOSED'


class EventType(str, Enum):
    CODE = 'CODE'
    DESAG = 'DESAG'
    ACADEMIC = 'ACADEMIC'
    TIMETABLE = 'TIMETABLE'


class AdministrativeOffice(Base):
    __tablename__ = 'administrative_offices'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(220), unique=True, index=True)
    office_type: Mapped[str] = mapped_column(String(80), index=True)
    dashboard_role: Mapped[str] = mapped_column(String(80), index=True)
    lead_title: Mapped[str | None] = mapped_column(String(180), nullable=True)
    lead_name: Mapped[str | None] = mapped_column(String(180), nullable=True)
    scope: Mapped[str | None] = mapped_column(String(220), nullable=True)
    reporting_line: Mapped[str | None] = mapped_column(String(220), nullable=True)
    key_modules: Mapped[str] = mapped_column(Text)
    can_publish_official: Mapped[bool] = mapped_column(Boolean, default=False)
    can_handle_tickets: Mapped[bool] = mapped_column(Boolean, default=False)
    can_view_analytics: Mapped[bool] = mapped_column(Boolean, default=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(180))
    email: Mapped[str] = mapped_column(String(180), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(50), index=True)
    region: Mapped[str | None] = mapped_column(String(120), nullable=True)
    programme: Mapped[str | None] = mapped_column(String(180), nullable=True)
    level: Mapped[str | None] = mapped_column(String(50), nullable=True)
    center_id: Mapped[int | None] = mapped_column(ForeignKey('study_centres.id'), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    center = relationship('StudyCentre', back_populates='users')


class StudyCentre(Base):
    __tablename__ = 'study_centres'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(180), unique=True, index=True)
    region: Mapped[str] = mapped_column(String(120), index=True)
    zone: Mapped[str | None] = mapped_column(String(120), nullable=True)
    town: Mapped[str | None] = mapped_column(String(120), nullable=True)
    coordinator_name: Mapped[str | None] = mapped_column(String(180), nullable=True)
    coordinator_phone: Mapped[str | None] = mapped_column(String(80), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    users = relationship('User', back_populates='center')


class Announcement(Base):
    __tablename__ = 'announcements'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(220), index=True)
    body: Mapped[str] = mapped_column(Text)
    notice_type: Mapped[str] = mapped_column(String(50), index=True)
    scope_type: Mapped[str] = mapped_column(String(50), default=ScopeType.ALL.value, index=True)
    region: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    programme: Mapped[str | None] = mapped_column(String(180), nullable=True, index=True)
    level: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    center_id: Mapped[int | None] = mapped_column(ForeignKey('study_centres.id'), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default='PUBLISHED')
    is_pinned: Mapped[bool] = mapped_column(Boolean, default=False)
    created_by_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    created_by = relationship('User')
    center = relationship('StudyCentre')


class Ticket(Base):
    __tablename__ = 'tickets'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    reference: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    subject: Mapped[str] = mapped_column(String(220), index=True)
    category: Mapped[str] = mapped_column(String(120), index=True)
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default=TicketStatus.OPEN.value, index=True)
    priority: Mapped[str] = mapped_column(String(40), default='NORMAL')
    student_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    assigned_to_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'), nullable=True)
    region: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    center_id: Mapped[int | None] = mapped_column(ForeignKey('study_centres.id'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship('User', foreign_keys=[student_id])
    assigned_to = relationship('User', foreign_keys=[assigned_to_id])
    center = relationship('StudyCentre')


class Event(Base):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(220), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    event_type: Mapped[str] = mapped_column(String(50), index=True)
    start_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    end_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    region: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    programme: Mapped[str | None] = mapped_column(String(180), nullable=True, index=True)
    level: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    center_id: Mapped[int | None] = mapped_column(ForeignKey('study_centres.id'), nullable=True)
    created_by_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    created_by = relationship('User')
    center = relationship('StudyCentre')


class DiscussionChannel(Base):
    __tablename__ = 'discussion_channels'
    __table_args__ = (UniqueConstraint('name', 'channel_type', name='uq_discussion_channel'),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(220), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    channel_type: Mapped[str] = mapped_column(String(80), index=True)
    region: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    programme: Mapped[str | None] = mapped_column(String(180), nullable=True, index=True)
    level: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    center_id: Mapped[int | None] = mapped_column(ForeignKey('study_centres.id'), nullable=True)
    is_moderated: Mapped[bool] = mapped_column(Boolean, default=True)
    created_by_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    created_by = relationship('User')
    center = relationship('StudyCentre')
    messages = relationship('DiscussionMessage', back_populates='channel', cascade='all, delete-orphan')


class DiscussionMessage(Base):
    __tablename__ = 'discussion_messages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    channel_id: Mapped[int] = mapped_column(ForeignKey('discussion_channels.id'), index=True)
    body: Mapped[str] = mapped_column(Text)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    channel = relationship('DiscussionChannel', back_populates='messages')
    author = relationship('User')


class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    actor_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'), nullable=True)
    action: Mapped[str] = mapped_column(String(180), index=True)
    resource_type: Mapped[str] = mapped_column(String(120), index=True)
    resource_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    actor = relationship('User')
