dev:
	poetry run python manage.py runserver
PORT ?= 8000
start:
		psql $(DATABASE_URL) < database.sql
		poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
