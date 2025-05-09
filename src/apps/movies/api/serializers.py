from typing import ClassVar

from rest_framework import serializers

from apps.movies.models import Country, Director, Genre, Movie


class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Country
        fields: ClassVar[list[str]] = ["url", "country"]


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields: ClassVar[list[str]] = ["url", "genre"]


class DirectorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Director
        fields: ClassVar[list[str]] = ["url", "director"]


class MovieSerializer(serializers.HyperlinkedModelSerializer):
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
