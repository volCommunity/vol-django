[![Build status](https://travis-ci.org/volCommunity/vol-django.svg?branch=master)](https://travis-ci.org/volCommunity/vol-django)
[![Coverage Status](https://coveralls.io/repos/github/volCommunity/vol-django/badge.svg?branch=master)](https://coveralls.io/github/volCommunity/vol-django?branch=master)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

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

Install Javascript dependencies using Yarn:

```shell
yarn install
```

### Running
#### Locally
Run the service locally, setting DEBUG to True allows using http instead of https,
and provides extra debugging output:
```shell
DEBUG=True python manage.py runserver
```

### In Heroku
_Travis deploys to Heroku on successful builds on master. Use these instructions
to deploy to another Heroko container._

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

### Creating tokens
Create them using the admin console, which you will be able to access locally at  <a href=http://localhost:8000/admin/authtoken>localhost:8000/admin/authtoken</a>.

## API
We run <a href=http://www.django-rest-framework.org>DRF</a>, which exposes a browesable API:
<a href="https://www.vol.community/api/">www.vol.community/api</a>. Alternatively use Swagger/OpenAPI at <a href="https://www.vol.community/api/swagger">www.vol.community/api/swagger</a>

Read only access can be accessed without tokens, mutating requires using basic auth or having
an API token.

Pass tokens by adding an Authorization header like so:

```shell
curl -X DELETE https://www.vol.community/api/jobs/1 --header "Content-Type: application/json" -H 'Authorization: Token 9b13d4942b24dc0eb12eb77f3eaf37f23b250175'
```

If you are looking for a client, <a href=https://github.com/core-api>core-api</a> clients do
 a great job at exploring and formatting results, see http://www.django-rest-framework.org/topics/api-clients for more examples. ie:

```python
 In [1]: from coreapi import Client
 In [2]: client = Client()
 In [3]: client.get('localhost:8000/api')
 In [4]: client.get('http://localhost:8000/api')
 Out[4]:
 OrderedDict([('labels', 'http://localhost:8000/api/labels'),
              ('organisations',
               'http://localhost:8000/api/organisations'),
              ('sites', 'http://localhost:8000/api/sites'),
              ('jobs', 'http://localhost:8000/api/jobs')])

 In [5]: client.get('http://localhost:8000/api/jobs')
 Out[5]:
 OrderedDict([('count', 4),
              ('next', None),
              ('previous', None),
              ('results',
               [OrderedDict([('id', 3),
                             ('title', 'Companion Volunteer'),
                             ('text',
                              'Provide safe companionship and support to the person with dementia for 1-2 hours weekly or fortnightly. This may include (but is not limited to) tasks such as visiting a cafe or library, going for a walk, making a cup of tea, reading the newsp aper together, watching sport etc. Police check required. TRAINING: Initial induction of two 2-hour sessions and ongoing o ptional training throughout the year. How to Apply'),
                             ('labels', [5]),
                             ('organisation',
                              OrderedDict([('id', 2),
                                           ('name', 'Dementia Canterbury'),
                                           ('region', 'canterbury'),
                                           ('city', 'christchurch'),
                                           ('url',
                                            'https://www.dementiacanterbury.org.nz/'),
                                           ('added', '2017-08-01')])),
                             ('sites', [2]),
                             ('country', 'new zealand'),
                             ('region', 'wellington'),
                             ('added', '2017-09-12'),
                             ('url',
                              'https://dogoodjobs.co.nz/jobs/companion-volunteer'),
                             ('seen', 0)]),
                <SNIP>
```