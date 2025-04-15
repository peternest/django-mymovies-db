# Generated by Django 5.2 on 2025-04-15 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_alter_movie_kp_rating_alter_movie_my_rating_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ['country'], 'verbose_name': 'Country', 'verbose_name_plural': 'Countries'},
        ),
        migrations.AlterModelOptions(
            name='director',
            options={'ordering': ['director'], 'verbose_name': 'Director', 'verbose_name_plural': 'Directors'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ['genre'], 'verbose_name': 'Genre', 'verbose_name_plural': 'Genres'},
        ),
        migrations.AlterModelOptions(
            name='movie',
            options={'ordering': ['title'], 'verbose_name': 'Movie', 'verbose_name_plural': 'Movies'},
        ),
        migrations.AlterField(
            model_name='movie',
            name='poster',
            field=models.ImageField(blank=True, default='images/_PosterPlaceholder.jpg', upload_to='images/', verbose_name='Poster'),
        ),
    ]
