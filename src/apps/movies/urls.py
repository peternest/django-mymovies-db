from django.urls import path

from apps.movies import views

urlpatterns = [
    path("top100/", views.MoviesListView.as_view(is_series=False)),
    path("series-top50/", views.MoviesListView.as_view(is_series=True)),
    path("<int:pk>/", views.MoviesDetailView.as_view()),
    path("add/", views.add_movie),
    path("add_country/", views.add_country),
    path("add_director/", views.add_director),
    path("add_genre/", views.add_genre),
    path("", views.MoviesRedirectView.as_view()),
]
