from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    BackgroundTasks
)

from sqlalchemy.orm import Session

from app.auth import verify_api_key
from app.database import get_db
from app.models.movie import Movie
from app.schemas.movie import MovieCreate, MovieResponse


router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)


def process_file(filename: str):
    print(f"Processing uploaded file: {filename}")


@router.post(
    "",
    status_code=201,
    response_model=MovieResponse
)
def create_movie(
    movie: MovieCreate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key)
):

    db_movie = Movie(**movie.model_dump())

    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)

    return db_movie


@router.get(
    "",
    response_model=list[MovieResponse]
)
def get_movies(
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key)
):

    return (
        db.query(Movie)
        .filter(Movie.is_active == True)
        .all()
    )


@router.get(
    "/{movie_id}",
    response_model=MovieResponse
)
def get_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key)
):

    movie = (
        db.query(Movie)
        .filter(Movie.id == movie_id)
        .first()
    )

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    return movie


@router.put(
    "/{movie_id}",
    response_model=MovieResponse
)
def update_movie(
    movie_id: int,
    data: MovieCreate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key)
):

    movie = (
        db.query(Movie)
        .filter(Movie.id == movie_id)
        .first()
    )

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    movie.title = data.title
    movie.genre = data.genre
    movie.rating = data.rating
    movie.watched = data.watched

    db.commit()
    db.refresh(movie)

    return movie


@router.delete("/{movie_id}")
def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key)
):

    movie = (
        db.query(Movie)
        .filter(Movie.id == movie_id)
        .first()
    )

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    # Soft Delete
    movie.is_active = False

    db.commit()

    return {
        "message": "Movie deleted successfully"
    }


@router.post("/upload")
async def upload_movie_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    _: str = Depends(verify_api_key)
):

    allowed_extensions = [
        ".pdf",
        ".jpg",
        ".png"
    ]

    extension = Path(
        file.filename
    ).suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, JPG and PNG files are allowed"
        )

    upload_path = (
        f"app/uploads/{file.filename}"
    )

    with open(
        upload_path,
        "wb"
    ) as buffer:

        content = await file.read()
        buffer.write(content)

    background_tasks.add_task(
        process_file,
        file.filename
    )

    return {
        "message": "File uploaded successfully",
        "filename": file.filename
    }