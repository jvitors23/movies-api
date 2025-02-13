venv:
	python3 -m venv .venv

test:
	pytest movies_api/apps --cov

migrate:
	python manage.py makemigrations && python manage.py migrate

rollback:
	python manage.py reset_db --no-input

super:
	python manage.py createsuperuser

show_urls:
	python manage.py show_urls
