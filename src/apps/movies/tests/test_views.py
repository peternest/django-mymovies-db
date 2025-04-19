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
    c = Country.objects.get(country="BrandNewCountry")

    assert response.status_code == 200
    assert Country.objects.count() == count_before + 1
    assert c.country == "BrandNewCountry"


def test_add_director(rf: RequestFactory) -> None:
    request = rf.post("/movies/add_director/", {"director": "DDD"})
    request.user = AnonymousUser()
    count_before = Director.objects.count()

    response = add_director(request)
    d = Director.objects.get(director="DDD")

    assert response.status_code == 200
    assert Director.objects.count() == count_before + 1
    assert d.director == "DDD"


def test_add_genre(rf: RequestFactory) -> None:
    request = rf.post("/movies/add_genre/", {"genre": "GGG"})
    request.user = AnonymousUser()
    count_before = Genre.objects.count()

    response = add_genre(request)
    g = Genre.objects.get(genre="GGG")

    assert response.status_code == 200
    assert Genre.objects.count() == count_before + 1
    assert g.genre == "GGG"


def test_add_dublicate_country_not_allowed(rf: RequestFactory) -> None:
    request = rf.post("/movies/add_country/", {"country": "BrandNewCountry"})
    request.user = AnonymousUser()
    count_before = Country.objects.count()

    _ = add_country(request)
    response = add_country(request)
    cnt = Country.objects.filter(country="BrandNewCountry").count()

    assert response.status_code == 200
    assert Country.objects.count() == count_before + 1
    assert cnt == 1


def test_get_countries_as_json(rf: RequestFactory) -> None:
    request = rf.get("/movies/get_countries/")
    request.user = AnonymousUser()

    response = get_objlist(request, "country")
    dic = json.loads(response.content)

    assert response.status_code == 200
    assert dic["success"] is True
    assert Country.objects.count() == len(dic["objlist"])


def test_add_movie(rf: RequestFactory) -> None:
    country = Country.objects.create(country="Новая страна")
    director = Director.objects.create(director="Миклухо Маклай")
    genre = Genre.objects.create(genre="Новый жанр")

    request = rf.post("/movies/add_movie/", {
        "title": "Жара в Египте",
        "release_year": 2012,
        "num_of_seasons": 1,
        "countries": [country.id],
        "directors": [director.id],
        "genres": [genre.id],
        "description": "Обалденный фильм!",
        "my_rating": 7,
        "kp_rating": 7
    })
    request.user = AnonymousUser()
    count_before = Movie.objects.count()

    response = add_movie(request)
    m = Movie.objects.get(title="Жара в Египте")

    assert response.status_code == 302
    assert Movie.objects.count() == count_before + 1
    assert m.release_year == 2012
    assert m.my_rating == 7
    assert m.kp_rating == 7
    assert m.description == "Обалденный фильм!"
    assert m.countries.all()[0].country == "Новая страна"
    assert m.directors.all()[0].director == "Миклухо Маклай"
    assert m.genres.all()[0].genre == "Новый жанр"
