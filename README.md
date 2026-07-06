# UCC CoDE Connect MVP

A starter web/PWA-style management and communication platform for the University of Cape Coast College of Distance Education, with a dedicated DESAG module from national to regional and centre levels.

## What is included

- Role-based login
- Official CoDE announcements
- DESAG announcements and activities
- Study centre directory
- Timetable and deadline records
- Student ticketing/helpdesk
- Discussion channels and messages
- Official link hub for MyUCC, eLearning, and CoDE website
- Basic management dashboard counts
- Administrative office dashboard register
- Dashboards for executive board, directorate, campus, department, departmental registration, unit, section, zonal/regional, and study centre roles
- Seed demo accounts

## Demo accounts

| Role | Email | Password |
|---|---|---|
| CoDE Admin | admin@codeconnect.app | Admin@123 |
| College Provost | provost@codeconnect.app | Provost@123 |
| College Registrar | registrar@codeconnect.app | Registrar@123 |
| Director | director@codeconnect.app | Director@123 |
| Head of Department | hod@codeconnect.app | Hod@12345 |
| Departmental Registration Officer, Education | dro.education@codeconnect.app | Dro@12345 |
| Departmental Registration Officer, Maths and Science | dro.mathscience@codeconnect.app | Dro@12345 |
| Departmental Registration Officer, Business | dro.business@codeconnect.app | Dro@12345 |
| Departmental Registration Officer, Arts and Social Science Education | dro.arts@codeconnect.app | Dro@12345 |
| Examinations Head | exams@codeconnect.app | Exams@123 |
| College Finance Officer, Executive Board | finance@codeconnect.app | Finance@123 |
| DESAG National | desag.national@codeconnect.app | Desag@123 |
| Regional Coordinator | coordinator@codeconnect.app | Coord@123 |
| Tutor | tutor@codeconnect.app | Tutor@123 |
| Student Support | support@codeconnect.app | Support@123 |
| Student | student@codeconnect.app | Student@123 |

Change or remove these accounts before production use.

## Administrative dashboards included

The MVP now includes a dedicated **Admin Offices** module. It registers the offices that should have dashboards in the production system:

- College Provost Office
- College Registrar Office
- College Finance Office, treated as part of the Executive Board
- Education and Business Programmes Directorate
- Admissions, Mathematics and Science Programmes Directorate
- Dominase Campus Directorate
- Agona Nyakrom Campus Directorate
- Greater Accra Campus Directorate
- Education Programmes Department
- Mathematics and Science Programmes Department
- Business Programmes Department
- Arts and Social Science Education Department
- Departmental Registration Office - Education Programmes
- Departmental Registration Office - Mathematics and Science Programmes
- Departmental Registration Office - Business Programmes
- Departmental Registration Office - Arts and Social Science Education
- Postgraduate Unit
- Switch Programme Unit
- Non-Residential Programme Unit
- Admissions Section
- RPDS
- Examination Section
- E-Learning and Quality Assurance Unit
- Student Support Services and Counselling Unit
- Teaching Practice and Project Work Unit
- SRMU
- Procurement Section
- Zonal and Regional Coordination Dashboards
- Study Centre Coordination Dashboards

Payment, registration, result checking, and core student records should remain linked to approved UCC systems unless UCC provides an official API.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

## Render deployment

1. Push this folder to GitHub.
2. On Render, create a new Blueprint and select the repository.
3. Render will read `render.yaml` and create the web service and PostgreSQL database.
4. Set `SECRET_KEY` to a strong private value if you are not using Render's generated value.
5. After deployment, open the Render URL and log in with the demo admin account.
6. Remove or change demo accounts before going live.

## Production notes

This is an MVP starter, not the final production system. Before launch, add:

- Official UCC SSO or approved identity integration
- SMS and push notification service
- File upload scanning and storage policy
- Strong audit reporting
- Rate limiting
- Terms, privacy notice, and data retention policy
- Approval workflow for DESAG public notices
- PostgreSQL backups
- Moderation workflow for discussion rooms
- Integration approval from DICTS for any UCC portal links or APIs
