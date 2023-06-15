dev:
	poetry run python manage.py runserver
translate:
	poetry run python manage.py makemessages -l ru_RU
compile:
	poetry run python manage.py compilemessages
