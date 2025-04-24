
# My Movies Database

This is my pet project to keep track of my favorite movies and series.
Powered by the Django web framework.

## Key features

* To show the list of top 100 movies or series ordered by rating, title or release year.
* To filter the list of movies by countries, genres, directors or release years.
* To add a new movie/series into the database or modify an existing one.
* To add a poster image to a movie/series.
* To show/edit data using the REST api.

## How to install it on a local machine

This project requires Python 3.11. 
[Poetry](https://python-poetry.org/) is used to manage dependencies and should be installed also.

Clone the repo into any folder:
```
git clone https://github.com/peternest/django-mymovies-db.git <any-folder>
cd <any-folder>
```

Create a virtual environment and install python requirements:
```
poetry shell
poetry install --no-root
```

**Configure database**. 
Use can use docker-compose to run PostgreSQL in the container or use any supported DBMS on a local machine.
Copy `src/.env.sample` to `src/.env` and edit the latter according to your configuration.

If you prefere to use docker-compose, run:
```
docker compose up -d
```

In the poetry shell change to the `src` folder and run the following commands to make initial setup:
```
cd src
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
python manage.py compilemessages
```

If you want to load some initial data in RUSSIAN (about 100 movies), execute:
```
python manage.py loaddata data/my_fixture.json
```

Run the development server:
```
python manage.py runserver
```

Once the app is running, you can test it by navigating to http://localhost:8000.
