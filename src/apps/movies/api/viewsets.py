from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.movies.api.serializers import (
    CountrySerializer,
    DirectorSerializer,
    GenreSerializer,
    MovieRatingSerializer,
    MovieSerializer,
    UserSerializer,
)
from apps.movies.models import Country, Director, Genre, Movie, MovieRating


class CountryViewSet(viewsets.ModelViewSet):
    """API endpoint that allows countries to be viewed or edited."""

    queryset = Country.objects.all().order_by("country")
    serializer_class = CountrySerializer


class GenreViewSet(viewsets.ModelViewSet):
    """API endpoint that allows genres to be viewed or edited."""

    queryset = Genre.objects.all().order_by("genre")
    serializer_class = GenreSerializer


class DirectorViewSet(viewsets.ModelViewSet):
    """API endpoint that allows directors to be viewed or edited."""

    queryset = Director.objects.all().order_by("director")
    serializer_class = DirectorSerializer


class MovieViewSet(viewsets.ModelViewSet):
    """API endpoint that allows movies to be viewed or edited."""

    queryset = Movie.objects.all().order_by("-kp_rating")
    serializer_class = MovieSerializer


class MovieRatingViewSet(viewsets.ModelViewSet):
    """API endpoint that allows movie ratings to be viewed or edited."""

    queryset = MovieRating.objects.all().order_by("rating")
    serializer_class = MovieRatingSerializer


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint that allows users to be viewed or edited."""

    queryset = User.objects.all().order_by("username")
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
