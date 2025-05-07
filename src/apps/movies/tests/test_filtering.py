import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from apps.movies.models import Country, Movie
from apps.movies.views import MoviesListView


pytestmark = [pytest.mark.django_db]


def test_filter_movies_by_country(rf: RequestFactory) -> None:
    country_russia = Country.objects.create(country="Russia")
    country_usa = Country.objects.create(country="USA")

    movie1 = Movie.objects.create(title="Russian Movie", is_series=False, release_year=2020)
    movie2 = Movie.objects.create(title="American Movie", is_series=False, release_year=2021)

    movie1.countries.add(country_russia)
    movie2.countries.add(country_usa)

    # Simulate a GET request with the 'country' filter
    request = rf.get("/movies/index.html", {"country": "Russia"})
    request.user = AnonymousUser()
    view = MoviesListView()
    view.request = request

    # Get the filtered queryset
    queryset = view.get_queryset()

    assert queryset.count() == 1
    assert queryset.first() == movie1
    assert movie1.countries.get(id=country_russia.id).country == "Russia"
