from django.contrib import admin

from .models import Country, Director, Genre, Movie

admin.site.register(Country)
admin.site.register(Director)
admin.site.register(Genre)
admin.site.register(Movie)
