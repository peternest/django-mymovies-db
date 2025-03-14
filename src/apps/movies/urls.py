from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view()),
    path("<int:pk>/", views.DetailView.as_view()),
    path("add_movie/", views.add_movie),
]
