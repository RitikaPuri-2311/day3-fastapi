Movie Watchlist API

A backend project built using FastAPI, PostgreSQL, SQLAlchemy, and Alembic.
This project demonstrates a complete CRUD system with database integration and migrations.

Tech Stack
FastAPI
PostgreSQL
SQLAlchemy (ORM)
Alembic (Migrations)
Uvicorn

app/
│── main.py
│── database.py

models/
│── movie.py
│── __init__.py

routes/
│── movie.py
│── __init__.py

alembic/
│── versions/

Schema/
│── movies.py
│── __init__.py
    
Create database:

CREATE DATABASE movie_watchlist;

Set environment variable:

DATABASE_URL=postgresql://postgres:password@localhost:5432/movie_watchlist

Run Migrations
python -m alembic revision --autogenerate -m "create movies table"
python -m alembic upgrade head

Run Application
python -m uvicorn app.main:app --reload

Open API docs:

http://127.0.0.1:8000/docs

 API Endpoints
Method	Endpoint	Description
POST	/movies	Add a new movie
GET	/movies	Get all movies
GET	/movies/{id}	Get movie by ID
PUT	/movies/{id}	Update movie
DELETE	/movies/{id}	Soft delete movie

