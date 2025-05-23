# Generated by Django 5.2 on 2025-04-27 19:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0006_movierating"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="kp_rating",
            field=models.FloatField(
                default=0.0,
                validators=[
                    django.core.validators.MinValueValidator(0.0),
                    django.core.validators.MaxValueValidator(10.0),
                ],
                verbose_name="KP rating",
            ),
        ),
        migrations.AlterField(
            model_name="movie",
            name="my_rating",
            field=models.FloatField(
                default=0.0,
                validators=[
                    django.core.validators.MinValueValidator(0.0),
                    django.core.validators.MaxValueValidator(10.0),
                ],
                verbose_name="My rating",
            ),
        ),
        migrations.AlterField(
            model_name="movierating",
            name="rating",
            field=models.FloatField(
                default=0.0,
                validators=[
                    django.core.validators.MinValueValidator(0.0),
                    django.core.validators.MaxValueValidator(10.0),
                ],
                verbose_name="Movie rating",
            ),
        ),
    ]
