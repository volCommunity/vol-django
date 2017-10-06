# Vol::Django

Welcome! This project is in very early and experimental stage, and help in the following areas would be greatly appreciated!

How you could help:
* Someone who would like to add support for new countries, or a Python dev who loves crawler the web? We are also looking for help writing crawlers, have a look at <a href="github.com/volCommunity/vol-crawlers">vol-crawlers</a>.
* Designers: Please help this site look better!
* Front end or full stack developers with an opinion on how to make things better: feel free to look at or raise issues or PRs.

## Development
We serve everything from Django, static assets too, using Whitenoise. If speed becomes an issue moving static assets
to a CDN would be a quick win.
The current tech stack currently consists of Python, Django 1.11, Bootstrap 4, Django REST Framework, Django analytics and PostgreSQL. All these things
could change any moment as this is in prototyping stage.

### Installation
We use the amazing <a href=https://github.com/kennethreitz/pipenv>Pipenv</a> to manage <a href=http://docs.python-guide.org/en/latest/dev/virtualenvs/>virtualenvs:</a>

Install Pipenv to manage virtualenvs, if you do not have it installed:
```
pip install pipenv
```

When Pipenv is available we spawn a shell and install the projects dependencies in our Virtualenv:
```shell
pipenv shell && pipenv install
```

We use PostgreSQL. Run the Docker image if you do not wish to install it locally:

```shell
docker run -p 5432:5432 --name postgres-db -d postgres:latest
```

Set your DATABASE_URL so Django is able to find it:

```shell
export DATABASE_URL=postgres://postgres@localhost/vol
```

Create the tables needed:

```shell
python manage.py migrate
```

### Running
#### Locally
Run the service locally:
```shell
python manage.py runserver
```

### In Heroku
Assuming you have a Heroku login and installed the CLI, see
<a href=https://devcenter.heroku.com/articles/getting-started-with-python>Heroku:Getting Started</a> if you have are
not familiar with Heroku.

Create and configure the app::

```shell
heroku create
heroku config:set DJANGO_SECRET_KEY=YourSecretKey
```

Deploy the code:
```
git push heroku master
```

See if app is running, create tables:
```
heroku ps:scale web=1 && heroku run python manage.py migrate
```

Inspect and tail the logs:
```shell
heroku logs --tail
```

Or start a console:
```shell
heroku run python manage.py shell
```

## API
We run <a href=http://www.django-rest-framework.org>DRF</a>, which exposes a browesable API:
<a href="https://www.vol.community/api/">www.vol.community/api</a>.

If you are looking for a client, <a href=https://github.com/core-api>core-api</a> clients do
 a great job at exploring and formatting results, ie:

```shell
 ▶ coreapi get http://127.0.0.1:8000/api
    {
        "labels": "http://127.0.0.1:8000/apiv0.0.1/labels",
        "organisations": "http://127.0.0.1:8000/apiv0.0.1/organisations",
        "sites": "http://127.0.0.1:8000/apiv0.0.1/sites",
        "jobs": "http://127.0.0.1:8000/apiv0.0.1/jobs"
    }
```