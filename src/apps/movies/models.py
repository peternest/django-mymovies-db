from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    country = models.CharField(max_length=30, verbose_name=_("Country"), unique=True)

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")
        ordering = ("country",)

    def __str__(self) -> str:
        return self.country


class Genre(models.Model):
    genre = models.CharField(max_length=30, verbose_name=_("Genre"), unique=True)

    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")
        ordering = ("genre",)

    def __str__(self) -> str:
        return self.genre


class Director(models.Model):
    director = models.CharField(max_length=30, verbose_name=_("Director"), unique=True)

    class Meta:
        verbose_name = _("Director")
        verbose_name_plural = _("Directors")
        ordering = ("director",)

    def __str__(self) -> str:
        return self.director


class Movie(models.Model):
    # fmt: off
    title = models.CharField(
        max_length=200,
        verbose_name=_("Title"),
    )
    title_orig = models.CharField(
        max_length=200,
        verbose_name=_("Title orig"),
        blank=True
    )
    is_series = models.BooleanField(
        verbose_name=_("Is series"),
        default=False
    )
    release_year = models.IntegerField(
        verbose_name=_("Release year"),
        default=2000,
        validators=[MinValueValidator(1900)]
    )
    series_last_year = models.IntegerField(
        verbose_name=_("Series last year"),
        blank=True,
        null=True,
        validators=[MinValueValidator(1900)]
    )
    num_of_seasons = models.IntegerField(
        verbose_name=_("Number of seasons"),
        default=1,
        validators=[MinValueValidator(1)]
    )
    countries = models.ManyToManyField(
        Country,
        verbose_name=_("Country"),
        blank=False
    )
    genres = models.ManyToManyField(
        Genre,
        verbose_name=_("Genre"),
        blank=False
    )
    directors = models.ManyToManyField(
        Director,
        verbose_name=_("Director"),
        blank=False
    )
    slogan = models.CharField(
        max_length=200,
        verbose_name=_("Slogan"),
        blank=True,
        default="-"
    )
    description = models.CharField(
        max_length=2000,
        verbose_name=_("Description"),
    )
    kp_rating = models.FloatField(
        verbose_name=_("KP rating"),
        default=0.0,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(10.0)
        ]
    )
    my_rating = models.FloatField(
        verbose_name=_("My rating"),
        default=0.0,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(10.0)
        ]
    )
    poster = models.ImageField(   # 600x900, relative to MEDIA_ROOT
        upload_to="images/",
        verbose_name=_("Poster"),
        blank=True,
        default="images/_PosterPlaceholder.jpg"
    )
    kinopoisk_url = models.URLField(
        verbose_name=_("Kinopoisk url"),
        blank=True
    )
    # fmt: on

    class Meta:
        verbose_name = _("Movie")
        verbose_name_plural = _("Movies")
        ordering = ("title",)
        constraints = (
            models.CheckConstraint(
                condition=models.Q(series_last_year__gte=models.F("release_year")),
                name="series_last_year_gte_release_year",
            ),
        )

    def __str__(self) -> str:
        return f"{self.title} ({self.release_year})"

    def get_countries(self) -> str:
        """To be used in Movie detail template."""
        return ", ".join(self.countries.values_list("country", flat=True))

    def get_genres(self) -> str:
        return ", ".join(self.genres.values_list("genre", flat=True))

    def get_directors(self) -> str:
        return ", ".join(self.directors.values_list("director", flat=True))

    def range_of_years(self) -> str:
        """Return "release_year — last_year" for series and "release_year" for movies."""
        if self.is_series and self.num_of_seasons > 1:
            last_year: str = f"{self.series_last_year}" if self.series_last_year else "..."
            return f"{self.release_year}—{last_year}"
        return f"{self.release_year}"


class MovieRating(models.Model):
    # fmt: off
    user = models.ForeignKey(
        User,
        verbose_name=_("User"),
        on_delete=models.CASCADE
    )
    movie = models.ForeignKey(
        Movie,
        verbose_name=_("Movie"),
        on_delete=models.CASCADE
    )
    rating = models.FloatField(
        verbose_name=_("Rating"),
        default=0.0,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(10.0)
        ]
    )
    review = models.TextField(
        max_length=1000,
        verbose_name=_("Review"),
        blank=True
    )
    # fmt: on

    class Meta:
        verbose_name = _("MovieRating")
        verbose_name_plural = _("MovieRatings")
        ordering = ("user", "movie")
        constraints = (models.UniqueConstraint(fields=["user", "movie"], name="unique_rating"),)

    def __str__(self) -> str:
        return f"{self.user} - {self.movie}"
