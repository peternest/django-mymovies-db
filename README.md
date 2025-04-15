
# My Movies Database

This is my pet project to keep track of my favorite movies and series.
Powered by Django web framework.

## Key features

* Show the list of top 100 movies or series ordered by title, rating or release year.
* Filter the list of movies by countries, genres, directors or release years.
* Add new movie/series into database or modify existing one.
* Show/edit data using REST api.

## Configuration

Configuration is stored in `src/.env`, for example see `src/.env.sample`
Movie database is stored in PostgreSQL, but you can use any supported DBMS, see `DATABASE_URL` parameter in `src/.env`.

## How to install on a local machine

This project requires Python 3.11+. [Poetry](https://python-poetry.org/) is used to manage dependencies.

Clone the repo into some folder:
```
$ git clone https://github.com/peternest/django-mymovies-db.git
```

Copy `src/.env.sample` to `src/.env` and edit the latter according to your configuration.

Probably you will create virtual environment first:
```
$ poetry shell
```

Install requirements:
```
$ poetry install --no-root
````

Change the folder to `src`, where `manage.py` lives:
```
$ cd src
```

If you want to load some initial data in RUSSIAN (about 100 movies), execute:
```
$ python manage.py loaddata data/my_fixture.json
```

Run the development server:
```
$ python manage.py runserver
```

Once the app is running, you can test it by navigating to http://localhost:8000.
