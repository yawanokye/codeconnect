from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.database import Base, SessionLocal, engine
from app.routers import admin_offices, announcements, auth_router, centres, dashboard, discussions, events, tickets, users
from app.seed import seed_database

settings = get_settings()

app = FastAPI(title=settings.app_name, version='0.1.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth_router.router)
app.include_router(admin_offices.router)
app.include_router(users.router)
app.include_router(centres.router)
app.include_router(announcements.router)
app.include_router(tickets.router)
app.include_router(events.router)
app.include_router(discussions.router)
app.include_router(dashboard.router)

STATIC_DIR = Path(__file__).parent / 'static'
app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')


@app.on_event('startup')
def startup() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()


@app.get('/health')
def health():
    return {'status': 'ok', 'app': settings.app_name}


@app.get('/')
def index():
    return FileResponse(STATIC_DIR / 'index.html')


@app.get('/{full_path:path}')
def spa_fallback(full_path: str):
    if full_path.startswith('api/'):
        return {'detail': 'Not found'}
    return FileResponse(STATIC_DIR / 'index.html')
