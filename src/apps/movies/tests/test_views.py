import json

import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from apps.movies.models import Country, Director, Genre, Movie
from apps.movies.views import add_country, add_director, add_genre, add_movie, get_objlist


pytestmark = [pytest.mark.django_db]


def test_add_country(rf: RequestFactory) -> None:
    request = rf.post("/movies/add_country/", {"country": "BrandNewCountry"})
    request.user = AnonymousUser()
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


def test_add_movie_with_related_fields(rf: RequestFactory) -> None:
    country = Country.objects.create(country="TestCountry")
    director = Director.objects.create(director="TestDirector")
    genre = Genre.objects.create(genre="TestGenre")

    request = rf.post("/movies/add_movie/", {
        "title": "Test Movie",
        "release_year": 2023,
        "num_of_seasons": 1,
        "countries": [country.id],
        "directors": [director.id],
        "genres": [genre.id],
        "description": "A test movie description.",
        "my_rating": 8,
        "kp_rating": 7.5
    })
    request.user = AnonymousUser()
    count_before = Movie.objects.count()

    response = add_movie(request)
    movie = Movie.objects.get(title="Test Movie")

    assert response.status_code == 302
    assert Movie.objects.count() == count_before + 1
    assert movie.release_year == 2023
    assert movie.my_rating == 8
    assert movie.kp_rating == 7.5
    assert movie.description == "A test movie description."
    assert movie.countries.first().country == "TestCountry"
    assert movie.directors.first().director == "TestDirector"
    assert movie.genres.first().genre == "TestGenre"
