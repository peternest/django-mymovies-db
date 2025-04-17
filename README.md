
# My Movies Database

This is my pet project to keep track of my favorite movies and series.
Powered by the Django web framework.

## Key features

* To show the list of top 100 movies or series ordered by rating, title or release year.
* To filter the list of movies by countries, genres, directors or release years.
* To add a new movie/series into the database or modify an existing one.
* To add a poster image to a movie/series.
* To show/edit data using the REST api.

## Configuration

Configuration is stored in `src/.env`; for examples see `src/.env.sample`.
The movie database is stored in PostgreSQL but you can use any supported DBMS; see `DATABASE_URL` parameter in `src/.env`.

## How to install it on a local machine

This project requires Python 3.11+. [Poetry](https://python-poetry.org/) is used to manage dependencies.

Clone the repo into any folder:
```
git clone https://github.com/peternest/django-mymovies-db.git <any-folder>
```

Copy `src/.env.sample` to `src/.env` and edit the latter according to your configuration.

Probably you will want to create a virtual environment first. After that install requirements:
```
poetry shell
poetry install --no-root
```

Change to the `src` folder, where `manage.py` lives:
```
cd src
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
python manage.py runserver
```

If you want to load some initial data in RUSSIAN (about 100 movies), execute:
```
python manage.py loaddata data/my_fixture.json
```
Note: after loading initial data movie posters will be absent (not distibuted with project). You can place them into the `src/media/images` folder and add by editing movies. Preferrable size is 600x900 px. 

Run the development server:
```
python manage.py runserver
```

Once the app is running, you can test it by navigating to http://localhost:8000.
