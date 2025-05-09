import json
from typing import Final

import pytest
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory

from apps.movies.models import Country, Director, Genre, Movie, MovieRating
from apps.movies.views import (
    add_country,
    add_director,
    add_genre,
    add_movie,
    change_movie,
    get_objlist,
    movie_detail,
)


pytestmark = [pytest.mark.django_db]


def test_add_country_anon_user(rf: RequestFactory) -> None:
    request = rf.post("/movies/add_country/", {"country": "NewCountry"})
    request.user = AnonymousUser()
    count_before = Country.objects.count()

    response = add_country(request)

    assert response.status_code == 200
    assert Country.objects.count() == count_before + 1
    assert Country.objects.get(country="NewCountry").country == "NewCountry"


def test_add_country_regular_user(rf: RequestFactory) -> None:
    request = rf.post("/movies/add_country/", {"country": "BrandNewCountry"})
    request.user = User.objects.create(username="TestUser", password="pass")
    count_before = Country.objects.count()

    response = add_country(request)

    assert response.status_code == 200
    assert Country.objects.count() == count_before + 1
    assert Country.objects.get(country="BrandNewCountry").country == "BrandNewCountry"


def test_add_director(rf: RequestFactory) -> None:
    request = rf.post("/movies/add_director/", {"director": "DDD"})
    request.user = AnonymousUser()
    count_before = Director.objects.count()

    response = add_director(request)

    assert response.status_code == 200
    assert Director.objects.count() == count_before + 1
    assert Director.objects.get(director="DDD").director == "DDD"


def test_add_genre(rf: RequestFactory) -> None:
    request = rf.post("/movies/add_genre/", {"genre": "GGG"})
    request.user = AnonymousUser()
    count_before = Genre.objects.count()

    response = add_genre(request)

    assert response.status_code == 200
    assert Genre.objects.count() == count_before + 1
    assert Genre.objects.get(genre="GGG").genre == "GGG"


def test_add_dublicate_country_not_allowed(rf: RequestFactory) -> None:
    request = rf.post("/movies/add_country/", {"country": "DuplicateCountry"})
    request.user = AnonymousUser()
    count_before = Country.objects.count()

    # Add the country for the first time
    response1 = add_country(request)
    assert response1.status_code == 200

    # Attempt to add the same country again
    response2 = add_country(request)
    count_after = Country.objects.count()

    assert response2.status_code == 200
    assert count_after == count_before + 1
    assert Country.objects.filter(country="DuplicateCountry").count() == 1


def test_get_countries_as_json(rf: RequestFactory) -> None:
    Country.objects.create(country="Country1")
    Country.objects.create(country="Country2")

    request = rf.get("/movies/get_countries/")
    request.user = AnonymousUser()

    response = get_objlist(request, "country")
    data = json.loads(response.content)

    assert response.status_code == 200
    assert data["success"] is True
    assert len(data["objlist"]) == Country.objects.count()
    assert {"id": Country.objects.get(country="Country1").id, "name": "Country1"} in data["objlist"]
    assert {"id": Country.objects.get(country="Country2").id, "name": "Country2"} in data["objlist"]


def test_movie_detail_found(rf: RequestFactory) -> None:
    movie = Movie.objects.create(title="Test Movie")

    request = rf.get(f"/movies/{movie.id}/")
    request.user = AnonymousUser()
    response = movie_detail(request, pk=movie.id)

    assert response.status_code == 200


def test_movie_detail_not_found(rf: RequestFactory) -> None:
    request = rf.get("/movies/999/")
    request.user = AnonymousUser()
    response = movie_detail(request, pk=999)

    assert response.status_code == 302


def test_add_movie_with_related_fields(rf: RequestFactory) -> None:
    user: Final = User.objects.create(username="TestUser", password="pass")
    country: Final = Country.objects.create(country="TestCountry")
    director: Final = Director.objects.create(director="TestDirector")
    genre: Final = Genre.objects.create(genre="TestGenre")

    request = rf.post(
        "/movies/add_movie/",
        {
            "title": "Test Movie",
            "is_series": False,
            "release_year": 2023,
            "num_of_seasons": 1,
            "countries": [country.id],
            "directors": [director.id],
            "genres": [genre.id],
            "description": "A test movie description.",
            "kp_rating": 7.5,
            "rating": 6,
            "review": "Good movie!",
        },
    )

    request.user = user
    count_before = Movie.objects.count()

    response = add_movie(request)

    assert response.status_code == 302
    assert Movie.objects.count() == count_before + 1

    movie: Final = Movie.objects.filter(title="Test Movie").first()
    assert movie is not None
    assert movie.release_year == 2023
    assert movie.kp_rating == 7.5
    assert movie.description == "A test movie description."
    assert movie.countries.get(id=country.id).country == "TestCountry"
    assert movie.directors.get(id=director.id).director == "TestDirector"
    assert movie.genres.get(id=genre.id).genre == "TestGenre"

    mr: Final = MovieRating.objects.filter(movie=movie, user=user).first()
    assert mr is not None
    assert mr.rating == 6
    assert mr.review == "Good movie!"


def test_change_movie_with_related_fields(rf: RequestFactory) -> None:
    user: Final = User.objects.create(username="TestUser", password="pass")
    country: Final = Country.objects.create(country="TestCountry")
    director: Final = Director.objects.create(director="TestDirector")
    genre: Final = Genre.objects.create(genre="TestGenre")

    movie: Final = Movie.objects.create(
        title="Old Title",
        is_series=False,
        release_year=2020,
        description="Old description",
        kp_rating=5.0,
    )
    movie.countries.add(country)
    movie.directors.add(director)
    movie.genres.add(genre)
    MovieRating.objects.create(user=user, movie=movie, rating=5.0, review="Old review")

    request = rf.post(
        f"/movies/{movie.id}/change/",
        {
            "title": "New Title",
            "is_series": True,
            "release_year": 2023,
            "num_of_seasons": 2,
            "countries": [country.id],
            "directors": [director.id],
            "genres": [genre.id],
            "description": "New description",
            "kp_rating": 8.0,
            "rating": 9.0,
            "review": "New review",
        },
    )
    request.user = user

    response = change_movie(request, pk=movie.id)
    movie.refresh_from_db()
    rating: Final = MovieRating.objects.get(movie=movie, user=user)

    assert response.status_code == 302

    assert movie is not None
    assert movie.title == "New Title"
    assert movie.is_series is True
    assert movie.release_year == 2023
    assert movie.num_of_seasons == 2
    assert movie.description == "New description"
    assert movie.kp_rating == 8.0

    assert rating is not None
    assert rating.rating == 9.0
    assert rating.review == "New review"
