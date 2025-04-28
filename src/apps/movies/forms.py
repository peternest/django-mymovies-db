from typing import ClassVar

from django.forms import (
    FileInput,
    ModelForm,
    ModelMultipleChoiceField,
    NumberInput,
    SelectMultiple,
    Textarea,
    TextInput,
    URLField,
    URLInput,
)
from django.forms.widgets import Input
from django.utils.translation import gettext_lazy as _

from apps.movies.models import Country, Director, Genre, Movie


class CountryForm(ModelForm):
    class Meta:
        model = Country
        fields: ClassVar[list[str]] = ["country"]
        labels: ClassVar[dict[str, str]] = {
            "country": _("Country name")
        }
        widgets: ClassVar[dict[str, Input]] = {
            "country": TextInput(attrs={"class": "text-field"})
        }


class DirectorForm(ModelForm):
    class Meta:
        model = Director
        fields: ClassVar[list[str]] = ["director"]
        labels: ClassVar[dict[str, str]] = {
            "director": _("Director name")
        }
        widgets: ClassVar[dict[str, Input]] = {
            "director": TextInput(attrs={"class": "text-field"})
        }


class GenreForm(ModelForm):
    class Meta:
        model = Genre
        fields: ClassVar[list[str]] = ["genre"]
        labels: ClassVar[dict[str, str]] = {
            "genre": _("Genre name")
        }
        widgets: ClassVar[dict[str, Input]] = {
            "genre": TextInput(attrs={"class": "text-field"})
        }


class MovieForm(ModelForm):
    required_css_class = "required"

    # M2M fields are placed here to set ordering.
    countries = ModelMultipleChoiceField(
        queryset=Country.objects.all().order_by("country"),
        label=_("Country"),
        widget=SelectMultiple(attrs={"size": 8})
    )
    genres = ModelMultipleChoiceField(
        queryset=Genre.objects.all().order_by("genre"),
        label=_("Genre"),
        widget=SelectMultiple(attrs={"size": 8})
    )
    directors = ModelMultipleChoiceField(
        queryset=Director.objects.all().order_by("director"),
        label=_("Director"),
        widget=SelectMultiple(attrs={"size": 8})
    )
    kinopoisk_url = URLField(
        label=_("Kinopoisk url"),
        required=False,
        widget=URLInput(attrs={"class": "url-field"}),
        assume_scheme="https"  # supress warning
    )

    class Meta:
        model = Movie
        fields: ClassVar[str] = [
            "title",
            "title_orig",
            "is_series",
            "release_year",
            "series_last_year",
            "num_of_seasons",
            "countries",
            "genres",
            "directors",
            "slogan",
            "description",
            "kp_rating",
            # "my_rating",
            "poster",
            "kinopoisk_url",
        ]
        labels: ClassVar[dict[str, str]] = {
            "title": _("Title"),
            "title_orig": _("Title orig"),
            "is_series": _("Is series"),
            "release_year": _("Release year"),
            "series_last_year": _("Series last year"),
            "num_of_seasons": _("Number of seasons"),
            "slogan": _("Slogan"),
            "description": _("Description"),
            # "my_rating": _("My rating"),
            "kp_rating": _("KP rating"),
            "poster": _("Poster"),
        }
        widgets: ClassVar[dict[str, Input]] = {
            "title": TextInput(attrs={"class": "text-field"}),
            "title_orig": TextInput(attrs={"class": "text-field"}),
            "release_year": NumberInput(attrs={"class": "release-field"}),
            "series_last_year": NumberInput(attrs={"class": "release-field"}),
            "num_of_seasons": NumberInput(attrs={"class": "release-field"}),
            "slogan": TextInput(attrs={"class": "text-field"}),
            "description": Textarea(attrs={"cols": 80, "rows": 5}),
            # "my_rating": NumberInput(attrs={"class": "float-field"}),
            "kp_rating": NumberInput(attrs={"class": "float-field"}),
            "poster": FileInput(attrs={"class": "text-field"})
        }
        error_messages: ClassVar[dict[str, dict[str, str]]] = {
            "title": {
                "max_length": _("This title is too long.")
            },
            "release_year": {
                "CHANGE_ME": _("Release year should be >= 1900.")
            }
        }
