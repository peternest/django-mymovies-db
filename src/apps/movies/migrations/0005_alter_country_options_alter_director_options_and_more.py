# Generated by Django 5.2 on 2025-04-24 13:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0004_alter_movie_my_rating"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="country",
            options={"ordering": ("country",), "verbose_name": "Country", "verbose_name_plural": "Countries"},
        ),
        migrations.AlterModelOptions(
            name="director",
            options={"ordering": ("director",), "verbose_name": "Director", "verbose_name_plural": "Directors"},
        ),
        migrations.AlterModelOptions(
            name="genre",
            options={"ordering": ("genre",), "verbose_name": "Genre", "verbose_name_plural": "Genres"},
        ),
        migrations.AlterModelOptions(
            name="movie",
            options={"ordering": ("title",), "verbose_name": "Movie", "verbose_name_plural": "Movies"},
        ),
    ]
