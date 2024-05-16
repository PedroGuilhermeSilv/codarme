runserver:
	@pdm run python manage.py runserver 0.0.0.0:8000

migrations:
	@pdm run python manage.py makemigrations

migrate:
	@pdm run python manage.py migrate

start_celery:
	@pdm run celery -A src.tamarcado.celery worker --loglevel=info