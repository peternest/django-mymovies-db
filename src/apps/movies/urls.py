from django.urls import path

from . import views

urlpatterns = [
    path("top100/", views.MoviesListView.as_view(is_series=False)),
    path("series-top50/", views.MoviesListView.as_view(is_series=True)),
    path("<int:pk>/", views.MoviesDetailView.as_view()),
    path("add/", views.add_movie),
    path("", views.MoviesRedirectView.as_view()),
]
