from typing import ClassVar

from django.contrib.auth.models import User
from rest_framework.serializers import HyperlinkedModelSerializer

from apps.movies.models import Country, Director, Genre, Movie, MovieRating


class CountrySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Country
        fields: ClassVar[list[str]] = ["url", "country"]


class GenreSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields: ClassVar[list[str]] = ["url", "genre"]


class DirectorSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Director
        fields: ClassVar[list[str]] = ["url", "director"]


class MovieSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Movie
        fields: ClassVar[list[str]] = [
            "title",
            "title_orig",
            "is_series",
            "release_year",
            "series_last_year",
            "num_of_seasons",
            "countries",
            "genres",
            "directors",
            "slogan",
            "description",
            "kp_rating",
            "poster",
            "kinopoisk_url",
        ]


class MovieRatingSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = MovieRating
        fields: ClassVar[list[str]] = [
            "user",
            "movie",
            "rating",
            "review",
        ]


class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields: ClassVar[list[str]] = ["url", "username", "email", "is_staff"]
