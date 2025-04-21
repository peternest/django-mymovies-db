import pytest

from apps.movies.models import Country, Director, Genre, Movie


@pytest.mark.django_db
def test_my_fixture_is_loaded() -> None:
    assert Country.objects.count() > 0
    assert Director.objects.count() > 0
    assert Genre.objects.count() > 0
    assert Movie.objects.count() > 0
