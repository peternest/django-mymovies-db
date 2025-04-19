from django.urls import include, path
from rest_framework import routers

from apps.movies.api.viewsets import CountryViewSet, DirectorViewSet, GenreViewSet, MovieViewSet


router = routers.DefaultRouter()
router.register("movies", MovieViewSet)
router.register("countries", CountryViewSet)
router.register("genres", GenreViewSet)
router.register("directors", DirectorViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
