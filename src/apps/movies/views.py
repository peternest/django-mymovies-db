from dataclasses import dataclass
from typing import Final, List

from django.db.models import Model
from django.db.models.manager import BaseManager
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, RedirectView

from apps.movies.forms import CountryForm, DirectorForm, GenreForm, MovieForm
from apps.movies.models import Country, Genre, Director, Movie


@dataclass
class Option:
    name: str
    value: str
    is_selected: bool


class MoviesListView(ListView):
    template_name = "movies/index.html"
    context_object_name = "top_100_movies"
    is_series = False

    OPTION_ALL: Final[str] = "Все"

    sort_list: List[Option] = [
        Option("рейтингу КП", "-kp_rating", False),
        Option("моему рейтингу", "-my_rating", False),
        Option("году выпуска", "-release_year", False),
        Option("алфавиту", "title", False)
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sort_list"] = self._make_sort_list()
        context["country_list"] = self._make_option_list(Country, "country")
        context["genre_list"] = self._make_option_list(Genre, "genre")
        context["director_list"] = self._make_option_list(Director, "director")
        context["is_series"] = self.is_series
        # print("Context {")
        # for k,v in context.items():
        #    print(f"  '{k}' = '{v}'")
        # print("}")
        return context

    def get_queryset(self) -> BaseManager[Movie]:
        country_value = self.request.GET.get("country", "")
        genre_value = self.request.GET.get("genre", "")
        director_value = self.request.GET.get("director", "")

        queryset = Movie.objects.filter(is_series=self.is_series)
        if country_value and country_value != self.OPTION_ALL:
            queryset = queryset.filter(countries__country=country_value)

        if genre_value and genre_value != self.OPTION_ALL:
            queryset = queryset.filter(genres__genre=genre_value)

        if director_value and director_value != self.OPTION_ALL:
            queryset = queryset.filter(directors__director=director_value)

        return queryset.order_by(self.get_ordering())

    def get_ordering(self) -> str:
        return self.request.GET.get("sort", "-kp_rating")

    def _make_sort_list(self) -> List[Option]:
        sort_value = self.request.GET.get("sort", "-kp_rating")
        for item in self.sort_list:
            item.is_selected = (item.value == sort_value)
        return self.sort_list

    def _make_option_list(self, model: Model, field_name: str) -> List[Option]:
        new_list: List[Option] = [
            Option(self.OPTION_ALL, self.OPTION_ALL, False)
        ]
        queryset = model.objects.all().order_by(field_name)
        for obj in queryset:
            new_list.append(Option(getattr(obj, field_name), getattr(obj, field_name), False))

        sel_value = self.request.GET.get(field_name, "")
        for item in new_list:
            item.is_selected = (item.value == sel_value)
        return new_list

    @classmethod
    def _debug_poster_path(cls, queryset: BaseManager[Movie]) -> None:
        for m in queryset:
            if m.poster:
                print(f"{m.title}, {m.poster.name}, {m.poster.path}")


class MoviesDetailView(DetailView):
    model = Movie
    template_name = "movies/detail.html"


class MoviesRedirectView(RedirectView):
    url = "/movies/top100/"


class APIMoviesRedirectView(RedirectView):
    url = "/api/movies/top100/"


def add_movie(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            # print(form.cleaned_data)
            form.save()
            return HttpResponseRedirect("/movies/")
        else:
            print(form.errors)
    else:
        form = MovieForm()
    return render(request, "movies/add_movie.html", {"form": form})


@csrf_exempt
def add_country(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CountryForm(request.POST)
        if form.is_valid():
            instance = form.save()
            return HttpResponse(f"Добавлен '{instance.country}'")
        else:
            return HttpResponse("Ошибка: такая страна уже существует!")
    else:
        form = CountryForm()
    return render(request, "movies/add_country.html", {"form": form})


@csrf_exempt
def add_director(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = DirectorForm(request.POST)
        if form.is_valid():
            instance = form.save()
            return HttpResponse(f"Добавлен '{instance.director}'")
        else:
            return HttpResponse("Ошибка: такой режиссер уже существует!")
    else:
        form = DirectorForm()
    return render(request, "movies/add_director.html", {"form": form})


@csrf_exempt
def add_genre(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = GenreForm(request.POST)
        if form.is_valid():
            instance = form.save()
            return HttpResponse(f"Добавлен '{instance.genre}'")
        else:
            return HttpResponse("Ошибка: такой жанр уже существует!")
    else:
        form = GenreForm()
    return render(request, "movies/add_genre.html", {"form": form})


def get_objlist(request: HttpRequest, field_name: str) -> JsonResponse:
    """Used by Javascript to retrieve the list of values for a model."""

    model: Model = ""
    if field_name == "country":
        model = Country
    elif field_name == "director":
        model = Director
    elif field_name == "genre":
        model = Genre

    queryset = model.objects.all().order_by(field_name)
    objlist = []
    for obj in queryset:
        objlist.append({
            "id": getattr(obj, "id"),
            "name": getattr(obj, field_name)
        })
    return JsonResponse({
        "success": True,
        "objlist": objlist
    })
