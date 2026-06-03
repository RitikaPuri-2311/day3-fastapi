from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal, get_db
from app.models.movie import Movie
from app.schemas.movie import MovieCreate, MovieResponse

router = APIRouter()

@router.post("/movies", status_code=201, response_model=MovieResponse)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):

    db_movie = Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)

    return db_movie

@router.get("/movies", response_model=list[MovieResponse])
def get_movies(db: Session = Depends(get_db)):

    return db.query(Movie).filter(Movie.is_active == True).all()

@router.get("/movies/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):

    movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    return movie

@router.put("/movies/{movie_id}", response_model=MovieResponse)
def update_movie(movie_id: int, data: MovieCreate, db: Session = Depends(get_db)):

    movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    movie.title = data.title
    movie.genre = data.genre
    movie.rating = data.rating
    movie.watched = data.watched

    db.commit()
    db.refresh(movie)

    return movie

@router.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):

    movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    movie.is_active = False
    db.commit()

    return {"message": "Movie deleted"}