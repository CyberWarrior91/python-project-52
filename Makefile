MANAGE := poetry run python manage.py

.PHONY: dev
dev:
	@$(MANAGE) runserver

.PHONY: translate
translate:
	@$(MANAGE) makemessages -l ru_RU

.PHONY: compile
compile:
	@$(MANAGE) compilemessages

.PHONY: migrations
migrations:
	@$(MANAGE) makemigrations

.PHONY: migrate
migrate:
	@$(MANAGE) migrate

.PHONY: shell
shell:
	@$(MANAGE) shell_plus --ipython

.PHONY: lint
lint:
	@poetry run flake8 task_manager
.PHONY: test
test:
	@poetry run coverage run --source='.' manage.py test
	@poetry run coverage xml
.PHONY: syncdb
syncdb:
	@$(MANAGE) syncdb --noinput

.PHONY: start	
start:
	@poetry install
	@$(MANAGE) makemigrations
	@$(MANAGE) migrate
	@$(MANAGE) runserver
