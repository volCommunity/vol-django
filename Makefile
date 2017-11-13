build:
	docker-compose build

test:
	docker-compose run -e DEBUG="" web scripts/wait-for-it.sh db:5432 -- pipenv run python manage.py test

lint:
	flake8

run:
	docker-compose up

list-flags:
	docker-compose run web pipenv run python manage.py waffle_flag -l
