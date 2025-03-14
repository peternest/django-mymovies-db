from django.forms import ModelForm, NumberInput, Textarea, TextInput, URLInput
from django.utils.translation import gettext_lazy as _

from .models import Movie


class MovieForm(ModelForm):
    # slug = CharField(validators=[validate_slug])

    class Meta:
        model = Movie
        fields = "__all__"
        labels = {
            "title": _("Title"),
            "title_orig": _("Title orig"),
            "release_year": _("Release year"),
            "countries": _("Country"),
            "genres": _("Genre"),
            "directors": _("Director"),
            "slogan": _("Slogan"),
            "description": _("Description"),
            "kp_rating": _("KP rating"),
            "my_rating": _("My rating"),
            "poster": _("Poster"),
            "kinopoisk_url": _('Kinopoisk url')
        }
        widgets = {
            "title": TextInput(attrs={'class': 'text-field'}),
            "title_orig": TextInput(attrs={'class': 'text-field'}),
            "release_year": NumberInput(attrs={'class': 'release-field'}),
            "slogan": TextInput(attrs={'class': 'text-field'}),
            "description": Textarea(attrs={"cols": 80, "rows": 5}),
            "kp_rating": NumberInput(attrs={'class': 'float-field'}),
            "my_rating": NumberInput(attrs={'class': 'float-field'}),
            # "poster": ImageField(),
            "kinopoisk_url": URLInput(attrs={'class': 'url-field'})
        }
