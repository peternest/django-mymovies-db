from apps.movies.models import Country, Genre, Director, Movie
from rest_framework import serializers


class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Country
        fields = ["url", "country"]


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ["url", "genre"]


class DirectorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Director
        fields = ["url", "director"]


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Movie
        fields = [
            "title",
            "title_orig",
            "release_year",
            "countries",
            "genres",
            "directors",
            "slogan",
            "description",
            "kp_rating",
            "my_rating",
            "kinopoisk_url"
        ]
