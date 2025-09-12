
# My Movies Database

This is my pet project to keep track of my favorite movies and series.
Powered by the Django web framework.

## Key features

* To show the list of top 100 movies or series ordered by rating, title or release year.
* To filter the list of movies by countries, genres, directors or release years.
* To add a new movie/series into the database or modify an existing one.
* To add a poster image to a movie/series.
* To add a user rating or review to a movie/series.
* To show/edit data using the REST api.

## Important

This project currently displays the UI only in Russian!

## How to install it on a local machine

Thе project requires Python 3.12. 
[Uv](https://docs.astral.sh/uv/) is used to manage dependencies and should be installed as well.

Clone the repo into any folder:
```
git clone https://github.com/peternest/django-mymovies-db.git <any-folder>
cd <any-folder>
```

Create a virtual environment and sync the project's dependencies with the environment:
```
uv sync
```

**Configure database**. You can use either docker-compose to run PostgreSQL in the container or any supported DBMS on a local machine (SQLite for example).

If you prefer to use docker, run:
```
docker compose up -d
```

Change to the `src` folder, copy `.env.sample` to `.env` and edit the latter according to your configuration:
```
cd src
cp .env.sample .env
```

Run the following commands to make an initial setup:
```
uv run python manage.py makemigrations
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py collectstatic
uv run python manage.py compilemessages
```

If you want to load some initial data in RUSSIAN (about 100 movies), execute:
```
uv run python manage.py loaddata data/my_fixture.json
```

Run the development server:
```
uv run python manage.py runserver
```

Once the app is running, you can test it by navigating to http://localhost:8000.
