from dataclasses import dataclass
from typing import Any, ClassVar, Final, LiteralString

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Model, Q
from django.db.models.manager import BaseManager
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, RedirectView

from apps.movies.forms import CountryForm, DirectorForm, GenreForm, MovieRatingForm
from apps.movies.models import Country, Director, Genre, Movie, MovieRating


@dataclass
class Option:
    name: str
    value: str
    is_selected: bool


def index(request: HttpRequest) -> HttpResponse:
    num_movies: Final = Movie.objects.filter(is_series=False).count()
    num_series: Final = Movie.objects.filter(is_series=True).count()
    num_users: Final = User.objects.filter(is_active=True).count()
    context = {
        "num_movies": num_movies,
        "num_series": num_series,
        "num_users": num_users,
    }
    return render(request, "index.html", context=context)


class MoviesListView(ListView):
    template_name = "movies/movie_list.html"
    context_object_name = "top_100_movies"
    is_series = False
    paginate_by = 25

    OPTION_ALL: Final[LiteralString] = _("All")

    EN_DASH: Final[LiteralString] = "–"  # noqa: RUF001

    sort_list: ClassVar[list[Option]] = [
        Option(_("by kp rating"), "-kp_rating", False),
        # Option(_("by my rating"), "-my_rating", False),  # noqa: ERA001
        Option(_("by release year"), "-release_year", False),
        Option(_("by title"), "title", False)
    ]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["sort_list"] = self._make_sort_list()
        context["country_list"] = self._make_option_list(Country, "country")
        context["genre_list"] = self._make_option_list(Genre, "genre")
        context["director_list"] = self._make_option_list(Director, "director")
        context["years_list"] = self._make_years_list()
        context["is_series"] = self.is_series
        return context

    def get_queryset(self) -> BaseManager[Movie]:
        country_value = self.request.GET.get("country", "")
        genre_value = self.request.GET.get("genre", "")
        director_value = self.request.GET.get("director", "")
        years_value = self.request.GET.get("years", "")

        queryset = Movie.objects.filter(is_series=self.is_series)
        if country_value and country_value != self.OPTION_ALL:
            queryset = queryset.filter(countries__country=country_value)

        if genre_value and genre_value != self.OPTION_ALL:
            queryset = queryset.filter(genres__genre=genre_value)

        if director_value and director_value != self.OPTION_ALL:
            queryset = queryset.filter(directors__director=director_value)

        if years_value and years_value != self.OPTION_ALL:
            years_list = years_value.split(self.EN_DASH)
            year_from = years_list[0]
            year_to = years_list[1]
            queryset = queryset.filter(Q(release_year__gte=year_from, release_year__lte=year_to))

        return queryset.order_by(self.get_ordering())

    def get_ordering(self) -> str:
        return self.request.GET.get("sort", "-kp_rating")

    def _make_sort_list(self) -> list[Option]:
        sort_value = self.request.GET.get("sort", "-kp_rating")
        for item in self.sort_list:
            item.is_selected = (item.value == sort_value)
        return self.sort_list

    def _make_years_list(self) -> list[Option]:
        new_list: list[Option] = [
            Option(self.OPTION_ALL, self.OPTION_ALL, False),
            Option(f"1900{self.EN_DASH}1949", f"1900{self.EN_DASH}1949", False),
        ]
        for year in range(1950, 2030, 10):
            yr = f"{year}{self.EN_DASH}{year + 9}"
            new_list.append(Option(yr, yr, False))

        years_value = self.request.GET.get("years", "")
        for item in new_list:
            item.is_selected = (item.value == years_value)
        return new_list

    def _make_option_list(self, model: Model, field_name: str) -> list[Option]:
        queryset = model.objects.all().order_by(field_name)

        new_list: list[Option] = [
            Option(self.OPTION_ALL, self.OPTION_ALL, False)
        ]
        new_list.extend(
            Option(getattr(obj, field_name), getattr(obj, field_name), False) for obj in queryset
        )

        sel_value = self.request.GET.get(field_name, "")
        for item in new_list:
            item.is_selected = (item.value == sel_value)
        return new_list


def movie_detail(request: HttpRequest, pk: int) -> HttpResponse:
    try:
        movie = get_object_or_404(Movie, pk=pk)
    except Http404:
        return HttpResponseRedirect("/movies/")

    user_rating = None
    if request.user.is_authenticated:
        record = movie.movierating_set.filter(user=request.user).first()
        if record:
            user_rating = record.rating
    return render(request, "movies/movie_detail.html", {"movie": movie, "user_rating": user_rating})


class MoviesRedirectView(RedirectView):
    url = "/movies/top100/"


class APIMoviesRedirectView(RedirectView):
    url = "/api/movies/top100/"


@login_required
def add_movie(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = MovieRatingForm(request.POST, request.FILES)
        if form.is_valid():
            movie_instance = form.save()
            if "rating" in form.cleaned_data or "review" in form.cleaned_data:
                MovieRating.objects.create(
                    user=request.user,
                    movie=movie_instance,
                    rating=form.cleaned_data.get("rating", 0.0),
                    review=form.cleaned_data.get("review", "")
                )
            return HttpResponseRedirect("/movies/top100/")
    else:
        form = MovieRatingForm()
    return render(request, "movies/add_movie.html", {"form": form, "is_edit": False})


@login_required
def change_movie(request: HttpRequest, pk: int) -> HttpResponse:
    movie_instance = get_object_or_404(Movie, pk=pk)
    rating_instance = MovieRating.objects.filter(user=request.user, movie=movie_instance).first()

    if request.method == "POST":
        form = MovieRatingForm(request.POST, request.FILES, instance=movie_instance, user=request.user)
        if form.is_valid():
            form.save()
            if "rating" in form.cleaned_data or "review" in form.cleaned_data:
                if rating_instance:
                    if "rating" in form.cleaned_data:
                        rating_instance.rating = form.cleaned_data["rating"]
                    if "review" in form.cleaned_data:
                        rating_instance.review = form.cleaned_data["review"]
                    rating_instance.save()
                else:
                    MovieRating.objects.create(
                        user=request.user,
                        movie=movie_instance,
                        rating=form.cleaned_data.get("rating", 0.0),
                        review=form.cleaned_data.get("review", "")
                    )
            return HttpResponseRedirect(f"/movies/{pk}/")
    else:
        form = MovieRatingForm(instance=movie_instance, user=request.user)
    return render(request, "movies/add_movie.html", {"form": form, "is_edit": True})


@csrf_exempt
def add_country(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CountryForm(request.POST)
        if form.is_valid():
            instance = form.save()
            return HttpResponse(_("Added") + f" '{instance.country}'")
        return HttpResponse(_("Error: such country already exists!"))
    form = CountryForm()
    return render(request, "movies/add_country.html", {"form": form})


@csrf_exempt
def add_director(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = DirectorForm(request.POST)
        if form.is_valid():
            instance = form.save()
            return HttpResponse(_("Added") + f" '{instance.director}'")
        return HttpResponse(_("Error: such director already exists!"))
    form = DirectorForm()
    return render(request, "movies/add_director.html", {"form": form})


@csrf_exempt
def add_genre(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = GenreForm(request.POST)
        if form.is_valid():
            instance = form.save()
            return HttpResponse(_("Added") + f" '{instance.genre}'")
        return HttpResponse(_("Error: such genre already exists!"))
    form = GenreForm()
    return render(request, "movies/add_genre.html", {"form": form})


def get_objlist(request: HttpRequest, field_name: str) -> JsonResponse:  # noqa: ARG001
    """Retrieve the list of values for a model (used by JS)."""
    model: Model = ""
    if field_name == "country":
        model = Country
    elif field_name == "director":
        model = Director
    elif field_name == "genre":
        model = Genre

    queryset = model.objects.all().order_by(field_name)
    objlist = [{
        "id": obj.id,
        "name": getattr(obj, field_name)
    } for obj in queryset]
    return JsonResponse({"success": True, "objlist": objlist})
