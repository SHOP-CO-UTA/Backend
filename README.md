## Prequisites

There are several prequisites to get started with.

### venv (optional but recommended)

Run the following command to create and activate a virtual environment.

#### On Linux/MacOS

```sh
python -m venv .venv
source .venv/bin/activate
```

#### On Windows

```sh
python -m venv .venv
.venv\Scripts\activate
```

### Install python requirements

To install the required dependencies, run the following command.

```sh
python -m pip install -r requirements.txt
```

## Development

### First time setup

#### Setup environment

Copy `.env.example` to `.env` and edit it to suit your needs. or Edit DATABASE in core/settings.py

#### Migrate database

```sh
python manage.py migrate
```

**NOTE** If errors happen, check your database connection environment variables. (If no database, please create new one)

Notes on creating/modifying tables in the database (PHONG)
- python manage.py makemigrations (Create the modified file (without touching the database)).
- python manage.py migrate (Apply changes to the database).

#### Run the server

To start the development server, run the following command.

```sh
python manage.py runserver
```

after that, visit `http://localhost:8000/api/docs/swagger` in your browser to see the API documentation.

### New module

#### Create new module

To create a new module, run the following command.

```sh
python manage.py startapp <module_name>
```

and add it to the `INTERNAL_APPS` list in `core/settings.py`.

after that, create some more files in your new module: `urls.py`, `serializers.py`. Details of those files are in the
next section.

#### Module structure

When created, the new module should have the following structure:

- `__init__.py` (should be empty)
- `apps.py` - This file contains the config for current module. It does not need to be changed, just leave it as it is.
- `models.py` - This file contains the models for current module. Write your models in this file.
- `serializers.py` - This file contains the serializers for current module.
- `tests.py` - This file contains the tests for current module. (optional)
- `views.py` - This file contains the views for current module.
- `urls.py` - This file contains the urls for current module. You should write the API in `views.py` and include it in
  this file.
