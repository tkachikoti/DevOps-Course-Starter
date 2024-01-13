# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

Link to Heroku App: [https://tnk-todo-app-c35bb5f5e658.herokuapp.com/](https://tnk-todo-app-c35bb5f5e658.herokuapp.com/)

## Table of contents

- [System Requirements](#system-requirements)
- [Dependencies](#dependencies)
- [Running the App](#running-the-app)
- [Building and Running Containers](#building-and-running-containers)

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of [Python](https://www.python.org/downloads/) version 3.7+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

The app relies on Trello to handle its to-do items and requires a Trello account, API key, and token to function. You will need to [create an account](https://trello.com/signup) on Trello, then generate an API key and token by following the [instructions here](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/). After creating the API key and token, assign them in the corresponding variables in the newly made `.env` file.

> [!WARNING]
> These credentials are tied to your account and need to be kept secret!

Following this, run the `trello_setup.py` script to configure other Trello-related variables in the `.env` file.

```bash
$ poetry run python setup_trello.py # (first time only)
```

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Building and Running Containers

### Test Container

To build and run the test container, use the following commands:

```
$ docker build --target test --tag todo-app:test .
$ docker run --rm todo-app:test
```

### Development Container

To build and run the development container, use the following commands:

```
$ docker build --target development --tag todo-app:dev .
$ docker run --env-file .env --publish 127.0.0.1:5000:5000 --mount type=bind,source="$(pwd)"/todo_app,target=/app/todo_app todo-app:dev
```

This will start a development container with hot reloading enabled. Any changes you make to your Python files will trigger Flask to reload the application automatically.

### Production Container

To build and run the production container, use the following commands:

```
$ docker build --target production --tag todo-app:prod .
$ docker run --env-file .env --publish 127.0.0.1:5000:8000 todo-app:prod
```

## Running the Tests

The project uses [pytest](https://docs.pytest.org/en/stable/) to run tests. To run the tests, run the following from root directory of the project:

```bash
$ poetry run pytest
```

If you want to run a specific test, you can specify the test file and the test function like this:

```bash
$ poetry run pytest todo_app/tests/test_todo_app.py::test_function_name
```

For example, the following command will only run the test_view_model_todo_items function in the test_todo_app.py file:

```bash
$ poetry run pytest todo_app/tests/test_unit.py::test_view_model_todo_items
```