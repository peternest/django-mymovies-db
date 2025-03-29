from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator


"""
> py manage.py makemigrations movies -- call after changes in the models
> py manage.py sqlmigrate movies 0001 -- show sql for the given migration
> py manage.py migrate -- perform migrations!

If the model field has blank=True, then required=False on the form field. Оtherwise, required=True.
"""


class Country(models.Model):
    country = models.CharField(
        max_length=30,
        verbose_name=_('Country'),
        unique=True
    )

    def __str__(self):
        return self.country

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')


class Genre(models.Model):
    genre = models.CharField(
        max_length=30,
        verbose_name=_('Genre'),
        unique=True
    )

    def __str__(self):
        return self.genre

    class Meta:
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')


class Director(models.Model):
    director = models.CharField(
        max_length=30,
        verbose_name=_('Director'),
        unique=True
    )

    def __str__(self):
        return self.director

    class Meta:
        verbose_name = _('Director')
        verbose_name_plural = _('Directors')


class Movie(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name=_('Title'),
    )
    title_orig = models.CharField(
        max_length=200,
        verbose_name=_('Title orig'),
        blank=True
    )
    is_series = models.BooleanField(
        verbose_name=_('Is series'),
        default=False
    )
    release_year = models.IntegerField(
        verbose_name=_('Release year'),
        default=2000,
        validators=[MinValueValidator(1900)]
    )
    series_last_year = models.IntegerField(
        verbose_name=_('Series last year'),
        blank=True,
        null=True,
        validators=[MinValueValidator(1900)]
    )
    num_of_seasons = models.IntegerField(
        verbose_name=_('Number of seasons'),
        default=1,
        validators=[MinValueValidator(1)]
    )
    countries = models.ManyToManyField(
        Country,
        verbose_name=_('Country'),
        blank=False
    )
    genres = models.ManyToManyField(
        Genre,
        verbose_name=_('Genre'),
        blank=False
    )
    directors = models.ManyToManyField(   # One to Many!?
        Director,
        verbose_name=_('Director'),
        blank=False
    )
    slogan = models.CharField(
        max_length=200,
        verbose_name=_('Slogan'),
        blank=True,
        default="-"
    )
    description = models.CharField(
        max_length=2000,
        verbose_name=_('Description'),
    )
    kp_rating = models.FloatField(
        verbose_name=_('KP rating'),
    )
    my_rating = models.FloatField(
        verbose_name=_('My rating'),
        blank=True,
        null=True
    )
    poster = models.ImageField(   # 600x900, relative to MEDIA_ROOT
        upload_to="images/",
        verbose_name=_('Poster'),
        blank=True
    )
    kinopoisk_url = models.URLField(
        verbose_name=_('Kinopoisk url'),
        blank=True
    )

    def __str__(self) -> str:
        return f"{self.title} ({self.release_year})"

    def get_countries(self) -> str:
        return ', '.join(self.countries.values_list('country', flat=True))

    def get_genres(self) -> str:
        return ', '.join(self.genres.values_list('genre', flat=True))

    def get_directors(self) -> str:
        return ', '.join(self.directors.values_list('director', flat=True))

    def range_of_years(self) -> str:
        if self.is_series and self.num_of_seasons > 1:
            last_year: str = f"{self.series_last_year}" if self.series_last_year else "..."
            return f"{self.release_year}—{last_year}"
        return f"{self.release_year}"

    class Meta:
        verbose_name = _('Movie')
        verbose_name_plural = _('Movies')
