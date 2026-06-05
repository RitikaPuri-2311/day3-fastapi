from fastapi import FastAPI

from app.database import Base, engine
from app.routes import movie
from app.middleware import log_requests

app = FastAPI(
    title="Movie Watchlist API",
    description="FastAPI + PostgreSQL + SQLAlchemy + Alembic",
    version="1.0.0"
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Request Logging Middleware
app.middleware("http")(log_requests)

# API Versioning
app.include_router(
    movie.router,
    prefix="/api/v1"
)

# Root Endpoint
@app.get("/")
def root():
    return {
        "message": "Welcome to Movie Watchlist API",
        "version": "v1"
    }