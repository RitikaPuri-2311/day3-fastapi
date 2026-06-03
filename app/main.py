from fastapi import FastAPI
from app.database import Base, engine
from app.routes import movie

app = FastAPI(
    title="Movie Watchlist API",
    description="FastAPI + PostgreSQL Movie Project",
    version="1.0.0"
)

# Create DB table
Base.metadata.create_all(bind=engine)

# ✅ Register routes
app.include_router(movie.router)