from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():

    response = client.get("/")

    assert response.status_code == 200


def test_create_movie():

    response = client.post(
        "/api/v1/movies",
        headers={
            "x-api-key": "movie123"
        },
        json={
            "title": "Interstellar",
            "genre": "Sci-Fi",
            "rating": 9.5,
            "watched": False
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Interstellar"
    assert data["genre"] == "Sci-Fi"


def test_get_movies():

    response = client.get(
        "/api/v1/movies",
        headers={
            "x-api-key": "movie123"
        }
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )


def test_get_movie_by_id():

    response = client.get(
        "/api/v1/movies/1",
        headers={
            "x-api-key": "movie123"
        }
    )

    assert response.status_code in [
        200,
        404
    ]


def test_update_movie():

    response = client.put(
        "/api/v1/movies/1",
        headers={
            "x-api-key": "movie123"
        },
        json={
            "title": "Updated Movie",
            "genre": "Drama",
            "rating": 8.5,
            "watched": True
        }
    )

    assert response.status_code in [
        200,
        404
    ]


def test_delete_movie():

    response = client.delete(
        "/api/v1/movies/1",
        headers={
            "x-api-key": "movie123"
        }
    )

    assert response.status_code in [
        200,
        404
    ]


def test_invalid_api_key():

    response = client.get(
        "/api/v1/movies",
        headers={
            "x-api-key": "wrong-key"
        }
    )

    assert response.status_code == 401


def test_movie_not_found():

    response = client.get(
        "/api/v1/movies/99999",
        headers={
            "x-api-key": "movie123"
        }
    )

    assert response.status_code == 404