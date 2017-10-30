# Introduction

Thank you for considering contributing to vol.community! It's people like you that can help make this project more awesome
than we could imagine.

Following these guidelines helps to communicate that you respect the time of the developers managing and developing this open source project.
In return, they should reciprocate that respect in addressing your issue, assessing changes, and helping you finalize your pull requests.

We are an open source project and we love to receive contributions from our community — you! There are many ways to contribute, examples are:

## Improve UI

## Improving documentation
Guides like the one you are reading a the moment are an important way for people to get on board. Once you start collaborating
and are all set it's easy to forget the challenges involved in getting up to speed with new knowledge domains and code bases. 

## Report Bugs
If you find a security vulnerability, do NOT open an issue. Email security@vol.community instead.

Report bugs at https://github.com/volCommunity/vol-django/issues

* If you can, provide detailed steps to reproduce the bug.
* If you don't have steps to reproduce the bug, just note your observations in as much detail as you can.
Questions to start a discussion about the issue are welcome.

## Solve Bugs
Any issue with labels "help wanted" and "bug" are fair game. Before you start work on one, please state your intention in the issue
to prevent others from duplicating your work!

# Ground Rules
* Create issues for any major changes and enhancements that you wish to make. Discuss things transparently and get community feedback.
* Keep feature versions as small as possible, preferably one new feature per version.
* Be welcoming to newcomers and encourage diverse new contributors from all backgrounds. See our [Code Of Conduct](href=https://github.com/volCommunity/vol-crawlers/blob/master/CODE_OF_CONDUCT.md>CODE_OF_CONDUCT.md)

# Your First Contribution
Not sure where to start contributing?

You can start looking at issues with label [help-wanted](https://github.com/volCommunity/vol-crawlers/issues?utf8=%E2%9C%93&q=is%3Aissue%20is%3Aopen%20label%3A%22help%20wanted%22%20).
As the project matures we'll have labels for beginner issues at [beginner-issue](https://github.com/volCommunity/vol-crawlers/issues?utf8=%E2%9C%93&q=is%3Aissue%20is%3Aopen%20label%3A%22beginner%20friendly%22) 
 which should only require a few lines of code, and a test or two.
Issues that would be a good first issue will be availble at [good-first-issue](https://github.com/volCommunity/vol-crawlers/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).

# Your First Pull Request
Working on your first Pull Request? You can learn how from this *free* series, [How to Contribute to an Open Source Project on GitHub](https://egghead.io/series/how-to-contribute-to-an-open-source-project-on-github).

# Suggesting a Feature
If you find yourself wishing for a feature that doesn't exist, you are probably not alone. There are bound to be others out there with similar needs.
Open an issue on our issues list on GitHub which describes the feature you would like to see, why you need it, and how it should work.

# Code Review Process
After your Pull Request has been reached anyone is able to suggest changes. Only suggestions by core contributors have to be
followed but do give any contructive feedback some thought.

Your Pull Request should have gotten feedback withing a week. If we suggest making changes we may close the pull requests if there is no activity withing 2 weeks.

# Community
You can chat with the core team IRC on [irc.freenode.net/#vol.community](https://kiwiirc.com/client/irc.freenode.net/#vol.community). We try to have office hours on Fridays.

# Development Workflow
The current tech stack currently consists of Python 3, Django 1.11, Bootstrap 4, Django REST Framework, Django analytics and PostgreSQL. All these things
could change any moment as this is in prototyping stage.

Make your life easier by installing the flake8 pre-commit hook, if flake8 fails, so will the Travis build.

```shell
flake8 --install-hook git            # Install the hook
git config --bool flake8.strict true # Prevent commit creation
```

## Installation
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

## Running
### Locally
Run the service locally, setting DEBUG to True allows using http instead of https,
and provides extra debugging output:
```shell
DJANGO_SECRET_KEY=YourSecretKey DEBUG=True python manage.py runserver
```

## In Heroku
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

## Creating tokens
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
