from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.auth import hash_password
from app.models import AdministrativeOffice, Announcement, DiscussionChannel, Event, StudyCentre, User


def seed_database(db: Session) -> None:
    if db.query(User).count() > 0:
        return

    centres = [
        StudyCentre(name='Cape Coast Study Centre', region='Central', zone='Southern', town='Cape Coast', coordinator_name='Centre Coordinator', coordinator_phone=''),
        StudyCentre(name='Kumasi Study Centre', region='Ashanti', zone='Middle', town='Kumasi', coordinator_name='Centre Coordinator', coordinator_phone=''),
        StudyCentre(name='Tamale Study Centre', region='Northern', zone='Northern', town='Tamale', coordinator_name='Centre Coordinator', coordinator_phone=''),
    ]
    db.add_all(centres)
    db.flush()

    offices = [
        AdministrativeOffice(
            name='College Provost Office', office_type='EXECUTIVE', dashboard_role='PROVOST',
            lead_title='College Provost', lead_name='Prof. Anokye Mohammed Adam',
            scope='College-wide leadership, performance monitoring, approvals, escalations, and strategic oversight',
            reporting_line='University Management',
            key_modules='Executive analytics, official approvals, unresolved ticket escalation, centre performance, DESAG liaison, audit trail',
            can_publish_official=True, can_handle_tickets=True, can_view_analytics=True,
        ),
        AdministrativeOffice(
            name='College Registrar Office', office_type='EXECUTIVE', dashboard_role='COLLEGE_REGISTRAR',
            lead_title='College Registrar', lead_name='Mr. Eugene K. Hesse',
            scope='Administrative coordination, records, correspondence, registry workflows, and operational compliance',
            reporting_line='College Provost',
            key_modules='Official notices, administrative tickets, user records, programme communication, audit trail, reports',
            can_publish_official=True, can_handle_tickets=True, can_view_analytics=True,
        ),
        AdministrativeOffice(
            name='Education and Business Programmes Directorate', office_type='DIRECTORATE', dashboard_role='DIRECTOR',
            lead_title='Director, Education and Business Programmes', lead_name='Prof. Joseph Tuffour Kwarteng',
            scope='Education and Business programme coordination',
            reporting_line='College Provost',
            key_modules='Programme dashboards, tutor coordination, timetable monitoring, academic notices, student issues by programme',
            can_publish_official=True, can_handle_tickets=True, can_view_analytics=True,
        ),
        AdministrativeOffice(
            name='Admissions, Mathematics and Science Programmes Directorate', office_type='DIRECTORATE', dashboard_role='DIRECTOR',
            lead_title='Director, Admissions, Mathematics and Science Programmes', lead_name='Prof. Emmanuel Kwasi Abu',
            scope='Admissions, Mathematics, and Science programme coordination',
            reporting_line='College Provost',
            key_modules='Admissions pipeline, programme dashboards, academic notices, applicant/student enquiries, analytics',
            can_publish_official=True, can_handle_tickets=True, can_view_analytics=True,
        ),
        AdministrativeOffice(
            name='Dominase Campus Directorate', office_type='CAMPUS', dashboard_role='CAMPUS_DIRECTOR',
            lead_title='Director, Dominase Campus', lead_name='Prof. Siaw Frimpong',
            scope='Campus-level coordination and service delivery', reporting_line='College Provost',
            key_modules='Campus notices, centre/session monitoring, tickets, student engagement, DESAG liaison, reports',
            can_publish_official=True, can_handle_tickets=True, can_view_analytics=True,
        ),
        AdministrativeOffice(
            name='Agona Nyakrom Campus Directorate', office_type='CAMPUS', dashboard_role='CAMPUS_DIRECTOR',
            lead_title='Director, Agona Nyakrom Campus', lead_name='Prof. Isaac Buabeng',
            scope='Campus-level coordination and service delivery', reporting_line='College Provost',
            key_modules='Campus notices, centre/session monitoring, tickets, student engagement, DESAG liaison, reports',
            can_publish_official=True, can_handle_tickets=True, can_view_analytics=True,
        ),
        AdministrativeOffice(
            name='Greater Accra Campus Directorate', office_type='CAMPUS', dashboard_role='CAMPUS_DIRECTOR',
            lead_title='Director, Greater Accra Campus', lead_name='Prof. Paul Nyagorme',
            scope='Campus-level coordination and service delivery', reporting_line='College Provost',
            key_modules='Campus notices, centre/session monitoring, tickets, student engagement, DESAG liaison, reports',
            can_publish_official=True, can_handle_tickets=True, can_view_analytics=True,
        ),
        AdministrativeOffice(
            name='Education Programmes Department', office_type='DEPARTMENT', dashboard_role='HEAD_OF_DEPARTMENT',
            lead_title='Head of Department, Education Programmes', lead_name='Prof. Vera Arhin',
            scope='Education programmes', reporting_line='Directorate',
            key_modules='Programme notices, tutor issues, academic complaints, course-level forums, performance alerts',
            can_publish_official=True, can_handle_tickets=True, can_view_analytics=True,
        ),
        AdministrativeOffice(
            name='Mathematics and Science Programmes Department', office_type='DEPARTMENT', dashboard_role='HEAD_OF_DEPARTMENT',
            lead_title='Head of Department, Maths and Science Programmes', lead_name='Prof. Valentina Akorful',
            scope='Mathematics and Science programmes', reporting_line='Directorate',
            key_modules='Programme notices, tutor issues, academic complaints, course-level forums, performance alerts',
            can_publish_official=True, can_handle_tickets=True, can_view_analytics=True,
        ),
        AdministrativeOffice(
            name='Business Programmes Department', office_type='DEPARTMENT', dashboard_role='HEAD_OF_DEPARTMENT',
            lead_title='Head of Department, Business Programmes', lead_name='Dr. Daisy Ofosuhene',
            scope='Business programmes', reporting_line='Directorate',
            key_modules='Programme notices, tutor issues, academic complaints, course-level forums, performance alerts',
            can_publish_official=True, can_handle_tickets=True, can_view_analytics=True,
        ),
        AdministrativeOffice(
            name='Arts and Social Science Education Department', office_type='DEPARTMENT', dashboard_role='HEAD_OF_DEPARTMENT',
            lead_title='Head of Department, Arts and Social Science Education', lead_name='Dr. Samuel Yaw Ampofo',
            scope='Arts and Social Science Education programmes', reporting_line='Directorate',
            key_modules='Programme notices, tutor issues, academic complaints, course-level forums, performance alerts',
            can_publish_official=True, can_handle_tickets=True, can_view_analytics=True,
        ),
        AdministrativeOffice(
            name='Departmental Registration Office - Education Programmes', office_type='DEPARTMENTAL_REGISTRATION', dashboard_role='DEPARTMENTAL_REGISTRATION_OFFICER',
            lead_title='Departmental Registration Officer', lead_name=None,
            scope='Registration support, departmental student list reconciliation, and registration issue tracking for Education Programmes',
            reporting_line='Head, Education Programmes/College Registrar',
            key_modules='Registration notices, registration tickets, student list reconciliation, course registration guidance, registration reports, audit trail',
            can_publish_official=True, can_handle_tickets=True, can_view_analytics=True,
        ),
        AdministrativeOffice(
            name='Departmental Registration Office - Mathematics and Science Programmes', office_type='DEPARTMENTAL_REGISTRATION', dashboard_role='DEPARTMENTAL_REGISTRATION_OFFICER',
            lead_title='Departmental Registration Officer', lead_name=None,
            scope='Registration support, departmental student list reconciliation, and registration issue tracking for Mathematics and Science Programmes',
            reporting_line='Head, Maths and Science Programmes/College Registrar',
            key_modules='Registration notices, registration tickets, student list reconciliation, course registration guidance, registration reports, audit trail',
            can_publish_official=True, can_handle_tickets=True, can_view_analytics=True,
        ),
        AdministrativeOffice(
            name='Departmental Registration Office - Business Programmes', office_type='DEPARTMENTAL_REGISTRATION', dashboard_role='DEPARTMENTAL_REGISTRATION_OFFICER',
            lead_title='Departmental Registration Officer', lead_name=None,
            scope='Registration support, departmental student list reconciliation, and registration issue tracking for Business Programmes',
            reporting_line='Head, Business Programmes/College Registrar',
            key_modules='Registration notices, registration tickets, student list reconciliation, course registration guidance, registration reports, audit trail',
            can_publish_official=True, can_handle_tickets=True, can_view_analytics=True,
        ),
        AdministrativeOffice(
            name='Departmental Registration Office - Arts and Social Science Education', office_type='DEPARTMENTAL_REGISTRATION', dashboard_role='DEPARTMENTAL_REGISTRATION_OFFICER',
            lead_title='Departmental Registration Officer', lead_name=None,
            scope='Registration support, departmental student list reconciliation, and registration issue tracking for Arts and Social Science Education',
            reporting_line='Head, Arts and Social Science Education/College Registrar',
            key_modules='Registration notices, registration tickets, student list reconciliation, course registration guidance, registration reports, audit trail',
            can_publish_official=True, can_handle_tickets=True, can_view_analytics=True,
        ),
        AdministrativeOffice(
            name='Postgraduate Unit', office_type='UNIT', dashboard_role='UNIT_COORDINATOR',
            lead_title='Coordinator, Postgraduate Unit', lead_name='Dr. Moses Segbenya',
            scope='Postgraduate student and programme coordination', reporting_line='College Registrar/Directorate',
            key_modules='Postgraduate notices, supervisor/student issues, deadlines, ticket queue, analytics',
            can_publish_official=True, can_handle_tickets=True, can_view_analytics=True,
        ),
        AdministrativeOffice(
            name='Switch Programme Unit', office_type='UNIT', dashboard_role='UNIT_COORDINATOR',
            lead_title='Coordinator, Switch Programme', lead_name='Dr. Justice G. Agyenim Boateng',
            scope='Switch programme coordination', reporting_line='College Registrar/Directorate',
            key_modules='Switch notices, cohort management, tickets, timetable, programme reports',
            can_publish_official=True, can_handle_tickets=True, can_view_analytics=True,
        ),
        AdministrativeOffice(
            name='Non-Residential Programme Unit', office_type='UNIT', dashboard_role='UNIT_COORDINATOR',
            lead_title='Coordinator, Non-Residential Programme', lead_name='Dr. Joanna Eva Dodoo',
            scope='Non-residential programme coordination', reporting_line='College Registrar/Directorate',
            key_modules='Non-residential notices, class/centre coordination, tickets, timetable, reports',
            can_publish_official=True, can_handle_tickets=True, can_view_analytics=True,
        ),
        AdministrativeOffice(
            name='College Finance Office', office_type='EXECUTIVE', dashboard_role='FINANCE_OFFICER',
            lead_title='College Finance Officer', lead_name='Kate Aba Sam',
            scope='Executive Board finance oversight, finance-related student support, and internal reporting. Payment remains linked to official UCC systems.',
            reporting_line='College Provost/Executive Board',
            key_modules='Executive finance analytics, fee guidance links, finance tickets, receipt guidance, finance reports, audit trail',
            can_publish_official=True, can_handle_tickets=True, can_view_analytics=True,
        ),
        AdministrativeOffice(
            name='Admissions Section', office_type='SECTION', dashboard_role='ADMISSIONS_HEAD',
            lead_title='Head, Admissions Section', lead_name='Cat. Dr. (Mrs) Sophia A. Abnory',
            scope='Admissions support and applicant/student transition issues', reporting_line='College Registrar',
            key_modules='Admissions announcements, applicant enquiries, admission tickets, dashboards, reports',
            can_publish_official=True, can_handle_tickets=True, can_view_analytics=True,
        ),
        AdministrativeOffice(
            name='RPDS', office_type='SECTION', dashboard_role='SECTION_HEAD',
            lead_title='Head, RPDS', lead_name='Ms. Miriam Danso-Mensah',
            scope='RPDS workflows and student/programme support where applicable', reporting_line='College Registrar',
            key_modules='Section notices, workflow tickets, documents, reports, analytics',
            can_publish_official=True, can_handle_tickets=True, can_view_analytics=True,
        ),
        AdministrativeOffice(
            name='Examination Section', office_type='SECTION', dashboard_role='EXAMS_HEAD',
            lead_title='Head, Examination Section', lead_name='Ms. Abigail Osarfo',
            scope='Examination notices, examination support, and exam-related ticket handling', reporting_line='College Registrar',
            key_modules='Exam notices, timetable links, exam tickets, centre exam reports, analytics',
            can_publish_official=True, can_handle_tickets=True, can_view_analytics=True,
        ),
        AdministrativeOffice(
            name='E-Learning and Quality Assurance Unit', office_type='UNIT', dashboard_role='UNIT_COORDINATOR',
            lead_title='Coordinator, E-Learning and Quality Assurance Unit', lead_name='Dr. Emmanuel Arthur-Nyarko',
            scope='E-learning support and quality assurance monitoring', reporting_line='College Provost/College Registrar',
            key_modules='E-learning issues, QA surveys, quality alerts, LMS links, tutor/session reports, analytics',
            can_publish_official=True, can_handle_tickets=True, can_view_analytics=True,
        ),
        AdministrativeOffice(
            name='Student Support Services and Counselling Unit', office_type='UNIT', dashboard_role='STUDENT_SUPPORT',
            lead_title='Coordinator, Student Support Services and Counselling Unit', lead_name='Dr. Joyce Kwakyewa Dankyi',
            scope='Student welfare, counselling, complaints, and support escalation', reporting_line='College Registrar',
            key_modules='Helpdesk, welfare tickets, counselling referrals, DESAG liaison, student support reports',
            can_publish_official=True, can_handle_tickets=True, can_view_analytics=True,
        ),
        AdministrativeOffice(
            name='Teaching Practice and Project Work Unit', office_type='UNIT', dashboard_role='UNIT_COORDINATOR',
            lead_title='Coordinator, Teaching Practice and Project Work Unit', lead_name='Dr. Vincent Minadzie',
            scope='Teaching practice and project work coordination', reporting_line='College Registrar/Directorate',
            key_modules='TP/project notices, supervision issues, placement/project tickets, reports, analytics',
            can_publish_official=True, can_handle_tickets=True, can_view_analytics=True,
        ),
        AdministrativeOffice(
            name='SRMU', office_type='SECTION', dashboard_role='SECTION_HEAD',
            lead_title='Head, SRMU', lead_name='Mr. Divine Selorm Wemegah',
            scope='SRMU workflows and student records/support where applicable', reporting_line='College Registrar',
            key_modules='Records/support tickets, notices, reports, audit trail, analytics',
            can_publish_official=True, can_handle_tickets=True, can_view_analytics=True,
        ),
        AdministrativeOffice(
            name='Procurement Section', office_type='SECTION', dashboard_role='PROCUREMENT_HEAD',
            lead_title='Head, Procurement Section', lead_name='Mr. Abraham Obeng',
            scope='Procurement workflows and logistics support for College operations', reporting_line='College Registrar/College Finance Office',
            key_modules='Procurement requests, logistics tickets, centre resource reports, audit trail, analytics',
            can_publish_official=False, can_handle_tickets=True, can_view_analytics=True,
        ),
        AdministrativeOffice(
            name='Zonal and Regional Coordination Dashboards', office_type='FIELD_OPERATIONS', dashboard_role='REGIONAL_COORDINATOR',
            lead_title='Zonal/Regional Coordinator', lead_name=None,
            scope='Northern, Middle, and Southern zonal coordination with regional reporting', reporting_line='College Registrar/Directorates',
            key_modules='Regional notices, centre monitoring, ticket escalation, DESAG regional liaison, attendance/session reports',
            can_publish_official=True, can_handle_tickets=True, can_view_analytics=True,
        ),
        AdministrativeOffice(
            name='Study Centre Coordination Dashboards', office_type='FIELD_OPERATIONS', dashboard_role='CENTER_COORDINATOR',
            lead_title='Study Centre Coordinator', lead_name=None,
            scope='Study centre activity, face-to-face sessions, local support, and centre-level reporting', reporting_line='Zonal/Regional Coordination',
            key_modules='Centre notices, attendance/session reporting, local tickets, centre timetable, DESAG centre liaison',
            can_publish_official=True, can_handle_tickets=True, can_view_analytics=True,
        ),
    ]
    db.add_all(offices)
    db.flush()

    users = [
        User(full_name='CoDE System Admin', email='admin@codeconnect.app', password_hash=hash_password('Admin@123'), role='CODE_ADMIN', region='Central', center_id=centres[0].id),
        User(full_name='College Provost', email='provost@codeconnect.app', password_hash=hash_password('Provost@123'), role='PROVOST', region='Central'),
        User(full_name='College Registrar', email='registrar@codeconnect.app', password_hash=hash_password('Registrar@123'), role='COLLEGE_REGISTRAR', region='Central'),
        User(full_name='Director of Programmes', email='director@codeconnect.app', password_hash=hash_password('Director@123'), role='DIRECTOR', region='Central'),
        User(full_name='Head of Department', email='hod@codeconnect.app', password_hash=hash_password('Hod@12345'), role='HEAD_OF_DEPARTMENT', region='Central', programme='B.Ed Accounting'),
        User(full_name='Education Programmes Registration Officer', email='dro.education@codeconnect.app', password_hash=hash_password('Dro@12345'), role='DEPARTMENTAL_REGISTRATION_OFFICER', region='Central', programme='Education Programmes'),
        User(full_name='Mathematics and Science Programmes Registration Officer', email='dro.mathscience@codeconnect.app', password_hash=hash_password('Dro@12345'), role='DEPARTMENTAL_REGISTRATION_OFFICER', region='Central', programme='Mathematics and Science Programmes'),
        User(full_name='Business Programmes Registration Officer', email='dro.business@codeconnect.app', password_hash=hash_password('Dro@12345'), role='DEPARTMENTAL_REGISTRATION_OFFICER', region='Central', programme='Business Programmes'),
        User(full_name='Arts and Social Science Education Registration Officer', email='dro.arts@codeconnect.app', password_hash=hash_password('Dro@12345'), role='DEPARTMENTAL_REGISTRATION_OFFICER', region='Central', programme='Arts and Social Science Education'),
        User(full_name='Examinations Head', email='exams@codeconnect.app', password_hash=hash_password('Exams@123'), role='EXAMS_HEAD', region='Central'),
        User(full_name='Finance Officer', email='finance@codeconnect.app', password_hash=hash_password('Finance@123'), role='FINANCE_OFFICER', region='Central'),
        User(full_name='DESAG National President', email='desag.national@codeconnect.app', password_hash=hash_password('Desag@123'), role='DESAG_NATIONAL'),
        User(full_name='Regional Coordinator', email='coordinator@codeconnect.app', password_hash=hash_password('Coord@123'), role='REGIONAL_COORDINATOR', region='Central', center_id=centres[0].id),
        User(full_name='Course Tutor', email='tutor@codeconnect.app', password_hash=hash_password('Tutor@123'), role='TUTOR', region='Central', programme='B.Ed Accounting', level='300', center_id=centres[0].id),
        User(full_name='Student Support Officer', email='support@codeconnect.app', password_hash=hash_password('Support@123'), role='STUDENT_SUPPORT', region='Central'),
        User(full_name='Demo Student', email='student@codeconnect.app', password_hash=hash_password('Student@123'), role='STUDENT', region='Central', programme='B.Ed Accounting', level='300', center_id=centres[0].id),
    ]
    db.add_all(users)
    db.flush()

    db.add_all([
        Announcement(
            title='Welcome to CoDE Connect',
            body='This official space is for verified CoDE notices, student support, study centre coordination, and academic reminders.',
            notice_type='OFFICIAL_CODE',
            scope_type='ALL',
            is_pinned=True,
            created_by_id=users[0].id,
        ),
        Announcement(
            title='DESAG National Orientation Planning',
            body='DESAG executives can use this module to coordinate national, regional, and centre-level student activities.',
            notice_type='DESAG',
            scope_type='NATIONAL',
            is_pinned=True,
            created_by_id=users[11].id,
        ),
    ])

    db.add_all([
        Event(
            title='Face-to-face session',
            description='Sample academic timetable entry for the Cape Coast Study Centre.',
            event_type='TIMETABLE',
            start_at=datetime.utcnow() + timedelta(days=7),
            end_at=datetime.utcnow() + timedelta(days=7, hours=3),
            region='Central',
            programme='B.Ed Accounting',
            level='300',
            center_id=centres[0].id,
            created_by_id=users[0].id,
        ),
        Event(
            title='DESAG regional welfare meeting',
            description='Sample DESAG event for student welfare coordination.',
            event_type='DESAG',
            start_at=datetime.utcnow() + timedelta(days=14),
            end_at=datetime.utcnow() + timedelta(days=14, hours=2),
            region='Central',
            center_id=centres[0].id,
            created_by_id=users[1].id,
        ),
    ])

    db.add_all([
        DiscussionChannel(
            name='B.Ed Accounting Level 300',
            description='Academic discussion room for course-related questions.',
            channel_type='PROGRAMME',
            region='Central',
            programme='B.Ed Accounting',
            level='300',
            center_id=centres[0].id,
            created_by_id=users[0].id,
        ),
        DiscussionChannel(
            name='DESAG National Forum',
            description='DESAG national student leadership and welfare discussion channel.',
            channel_type='DESAG',
            created_by_id=users[1].id,
        ),
    ])

    db.commit()
