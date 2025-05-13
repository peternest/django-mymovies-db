from django.urls import include, path
from rest_framework import routers

from apps.movies.api.viewsets import (
    CountryViewSet,
    DirectorViewSet,
    GenreViewSet,
    MovieRatingViewSet,
    MovieViewSet,
    UserViewSet,
)


router = routers.DefaultRouter()
router.register("movies", MovieViewSet)
router.register("movieratings", MovieRatingViewSet)
router.register("countries", CountryViewSet)
router.register("genres", GenreViewSet)
router.register("directors", DirectorViewSet)
router.register("users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
