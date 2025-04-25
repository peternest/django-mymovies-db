from typing import ClassVar

from django.contrib import admin
from django.forms import ModelForm, Textarea
from django.forms.widgets import Input

from apps.movies.models import Country, Director, Genre, Movie


admin.site.register(Country)
admin.site.register(Director)
admin.site.register(Genre)


class MovieAdminForm(ModelForm):
    class Meta:
        model = Movie
        fields = "__all__"
        widgets: ClassVar[dict[str, Input]] = {
            "description": Textarea(attrs={"rows": 5, "cols": 100}),
        }


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    form = MovieAdminForm

    list_display = ("title", "release_year", "is_series", "kp_rating")
    list_filter = ("is_series", "genres")
    search_fields = ("title",)

    fields = (
        "title",
        "title_orig",
        "is_series",
        ("release_year", "series_last_year", "num_of_seasons"),
        "countries",
        "genres",
        "directors",
        "slogan",
        "description",
        "my_rating",
        "kp_rating",
        "poster",
        "kinopoisk_url"
    )

