from dataclasses import dataclass
from typing import List

from django.db.models import Model
from django.db.models.manager import BaseManager
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .forms import MovieForm
from .models import Country, Genre, Director, Movie


OPTION_ALL = "Все"


@dataclass
class Option:
    name: str
    value: str
    is_selected: bool


sort_list: List[Option] = [
    Option("рейтингу КП", "-kp_rating", False),
    Option("моему рейтингу", "-my_rating", False),
    Option("году выпуска", "-release_year", False),
    Option("алфавиту", "title", False)
]


class IndexView(ListView):
    template_name = "movies/index.html"
    context_object_name = "top_100_movies"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sort_list"] = self._make_sort_list()
        context["country_list"] = self._make_option_list(Country, "country")
        context["genre_list"] = self._make_option_list(Genre, "genre")
        context["director_list"] = self._make_option_list(Director, "director")
        # print("Context {")
        # for k,v in context.items():
        #    print(f"  '{k}' = '{v}'")
        # print("}")
        return context

    def get_queryset(self):
        country_value = self.request.GET.get("country", "")
        genre_value = self.request.GET.get("genre", "")
        director_value = self.request.GET.get("director", "")

        queryset = Movie.objects.all()
        if country_value and country_value != OPTION_ALL:
            queryset = queryset.filter(countries__country=country_value)

        if genre_value and genre_value != OPTION_ALL:
            queryset = queryset.filter(genres__genre=genre_value)

        if director_value and director_value != OPTION_ALL:
            queryset = queryset.filter(directors__director=director_value)

        return queryset.order_by(self.get_ordering())

    def get_ordering(self):
        return self.request.GET.get("sort", "-kp_rating")

    def _make_sort_list(self):
        sort_value = self.request.GET.get("sort", "-kp_rating")
        for item in sort_list:
            item.is_selected = (item.value == sort_value)
        return sort_list

    def _make_option_list(self, model: Model, field_name: str) -> List[Option]:
        new_list: List[Option] = [
            Option(OPTION_ALL, OPTION_ALL, False)
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


class DetailView(DetailView):
    model = Movie
    template_name = "movies/detail.html"


def add_movie(request):
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
