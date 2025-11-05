from django.urls import path

from apps.movies import views


urlpatterns = [
    path("", views.index),
    path("top100/", views.MoviesListView.as_view(is_series=False)),
    path("series-top30/", views.MoviesListView.as_view(is_series=True)),
    path("<int:pk>/", views.movie_detail),
    path("add/", views.add_movie),
    path("<int:pk>/change/", views.change_movie),
    # ---
    path("add_country/", views.add_country),
    path("add_director/", views.add_director),
    path("add_genre/", views.add_genre),
    path("get_countries/", views.get_objlist, {"field_name": "country"}),
    path("get_directors/", views.get_objlist, {"field_name": "director"}),
    path("get_genres/", views.get_objlist, {"field_name": "genre"}),
]
