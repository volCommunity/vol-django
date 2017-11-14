build:
	docker-compose build

migrations:
	docker-compose run web scripts/wait-for-it.sh db:5432 -- pipenv run python manage.py makemigrations
	
shell:
	docker-compose run web scripts/wait-for-it.sh db:5432 -- pipenv run python manage.py shell

migrate:
	docker-compose run web scripts/wait-for-it.sh db:5432 -- pipenv run python manage.py migrate 

test:
	docker-compose run -e DEBUG="" web scripts/wait-for-it.sh db:5432 -- pipenv run python manage.py test

lint:
	flake8

run:
	docker-compose up

list-flags-local:
	docker-compose run web pipenv run python manage.py waffle_flag -l

list-flags-heroku:
	heroku run python manage.py waffle_flag -l
