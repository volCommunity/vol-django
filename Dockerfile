FROM python:3.6.3

RUN pip install pipenv

RUN mkdir /app
WORKDIR /app

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install

COPY . /app

EXPOSE 8000
CMD scripts/wait-for-it.sh db:5432 -- pipenv run python manage.py migrate && pipenv run python manage.py runserver 0.0.0.0:8000
