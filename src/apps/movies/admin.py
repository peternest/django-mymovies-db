from collections.abc import Mapping
from typing import Any, ClassVar

from django.contrib import admin
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.db import models
from django.forms import ModelChoiceField, ModelForm, Textarea
from django.forms.widgets import NumberInput, Widget
from django.http import HttpRequest

from apps.movies.models import Country, Director, Genre, Movie, MovieRating


type FormFieldType = Mapping[type[models.Field[Any, Any]], Mapping[str, Any]]

admin.site.register(Country)
admin.site.register(Director)
admin.site.register(Genre)


class MovieAdminForm(ModelForm):
    class Meta:
        model = Movie
        fields = "__all__"
        widgets: ClassVar[dict[str, Widget]] = {
            "description": Textarea(attrs={"rows": 5, "cols": 100}),
        }


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    form = MovieAdminForm

    list_display = ("title", "release_year", "is_series", "kp_rating")
    list_editable = ("kp_rating",)
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
        "kp_rating",
        "my_rating",
        "poster",
        "kinopoisk_url",
    )

    formfield_overrides: ClassVar[FormFieldType] = {
        models.FloatField: {"widget": NumberInput(attrs={"style": "width: 60px;"})}
    }


@admin.register(MovieRating)
class MovieRatingAdmin(admin.ModelAdmin):
    list_display = ("user", "movie", "rating")
    list_display_links = ("user",)
    list_editable = ("rating",)
    list_filter = ("user",)
    list_select_related = ("user", "movie")

    fields = ("user", "movie", "rating", "review")

    formfield_overrides: ClassVar[FormFieldType] = {
        models.FloatField: {"widget": NumberInput(attrs={"style": "width: 60px;"})}
    }

    # https://docs.djangoproject.com/en/5.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.formfield_for_foreignkey

    # TODO(peter): #001 - Remove these buttons!  # noqa: FIX002

    def formfield_for_foreignkey(
        self, db_field: models.ForeignKey, request: HttpRequest, **kwargs: Any
    ) -> ModelChoiceField | None:
        if db_field.name in ["user", "movie"]:
            ff = db_field.formfield(**kwargs)
            if ff:
                kwargs["widget"] = RelatedFieldWidgetWrapper(
                    widget=ff.widget,
                    rel=db_field.remote_field,
                    admin_site=self.admin_site,
                    can_add_related=False,
                    can_change_related=False,
                    can_view_related=False,
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
