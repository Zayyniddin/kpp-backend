# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from database import engine, ping_db
from models import base, warehouse, user
from routers import admin , guard, dispatcher, auth, admin_logs

def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth.router)
    app.include_router(admin.router)
    app.include_router(guard.router)
    app.include_router(dispatcher.router)
    app.include_router(admin_logs.router)

    @app.on_event("startup")
    def on_startup():
        ping_db()
        # base.Base.metadata.drop_all(bind=engine)
        base.Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully!")

    @app.get("/health", tags=["system"])
    def health():
        try:
            ping_db()
            return {"status": "ok", "database": "connected"}
        except Exception as e:
            return {"status": "error", "database_error": str(e)}

    return app

app = create_app()