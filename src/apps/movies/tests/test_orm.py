import pytest

from apps.movies.models import Country, Director, Genre, Movie


pytestmark = [pytest.mark.django_db]


def test_create_simple_objects() -> None:
    country = Country.objects.create(country="TestCountry")
    assert Country.objects.count() == 1
    assert country.country == "TestCountry"

    director = Director.objects.create(director="TestDirector")
    assert Director.objects.count() == 1
    assert director.director == "TestDirector"

    genre = Genre.objects.create(genre="TestGenre")
    assert Genre.objects.count() == 1
    assert genre.genre == "TestGenre"


def test_create_movie_with_defaults() -> None:
    movie = Movie.objects.create(title="Test Movie")

    assert Movie.objects.count() == 1
    assert movie.title == "Test Movie"
    assert movie.title_orig == ""
    assert movie.is_series is False
    assert movie.release_year == 2000
    assert movie.series_last_year is None
    assert movie.num_of_seasons == 1
    assert movie.countries.count() == 0
    assert movie.directors.count() == 0
    assert movie.genres.count() == 0
    assert movie.description == ""
    assert movie.slogan == "-"
    assert movie.kp_rating == 0.0
    assert movie.poster == "images/_PosterPlaceholder.jpg"
    assert movie.kinopoisk_url == ""
