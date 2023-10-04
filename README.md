### Hexlet tests and linter status:
[![Actions Status](https://github.com/CyberWarrior91/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/CyberWarrior91/python-project-52/actions)
[![Github Actions Status](https://github.com/CyberWarrior91/python-project-52/actions/workflows/pyci.yml/badge.svg)](https://github.com/hexlet-boilerplates/python-package/actions)
<a href="https://codeclimate.com/github/CyberWarrior91/python-project-52/maintainability"><img src="https://api.codeclimate.com/v1/badges/21debc5e41ccff9634e6/maintainability" /></a>
<a href="https://codeclimate.com/github/CyberWarrior91/python-project-52/test_coverage"><img src="https://api.codeclimate.com/v1/badges/21debc5e41ccff9634e6/test_coverage" /></a>

## Getting started

**Description:**

This is a simple Task Manager application, which makes it easier to create, update and delete task for your teammates. It also allows you to put status, label and executor on a task, user authorization is also included.
You can see how it works by following this <a href="https://python-project-52-production-882e.up.railway.app/">link</a>

## Usage

#### Clone the repository using this command:
```git clone https://github.com/CyberWarrior91/python-project-52.git```

**Requirements:**
 
 This app works on Django framework and uses Django in-build Django admin, Django filters, Django-bootstrap etc. libraries, as well as some side ones, so make sure to get all the dependencies installed on your machine before starting the application:
 
* python = "^3.8"
* django = "^4.2.2"
* django-admin = "^2.0.2"
* python-dotenv = "^1.0.0"
* dj-database-url = "^2.0.0"
* psycopg2-binary = "^2.9.6"
* gunicorn = "^20.1.0"
* django-bootstrap4 = "^23.1"
* django-crispy-forms = "^2.0"
* django-filter = "^23.2"
* rollbar = "^0.16.3"
* django-extensions = "^3.2.3"
* django-cors-headers = "^4.2.0"
* coverage = "^7.3.0"
* codecov = "^2.1.13"
* whitenoise = "^6.2.0"
* django-bootstrap-v5 = "^1.0.11"
* crispy-bootstrap4 = "^2022.1"

In addition, you need to have your *DATABASE_URL*, *SECRET_KEY*, *DEBUG* and *ROLLBAR_TOKEN* (if you use Rollbar) environment variables specified for both development and production environment in order for this application to work properly

## Makefile

In order to use commands from Makefile, you need to have **poetry** installed

Firstly, check your current pip version and upgrade it, if needed:

```python -m pip --version```

```python -m pip install --upgrade pip```

Then install Poetry via this link:

[Poetry installation](https://python-poetry.org/docs/)

After successful installation, you need to initiate new poetry package using this command:

```poetry init```

### Makefile commands:

```make install``` install poetry packages

```make dev``` starts the app on the local server in the development environment

```make start``` start the app in the production environment

```make migrations``` create migrations for your database

```make migrate``` apply migrations

