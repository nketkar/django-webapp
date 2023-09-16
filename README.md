## THE GEOKEY SERVICE

A few instructions on setting up the project for local development.

### Installation:

You will need to install both python and javascript/front-end dependencies for local development.

To install the python dependencies, in a virtual env do:

`pip installl -r requirements.txt`

For front end dependencies do(assuming you have node and npm installed in your system):

`npm install` to install.

Bootstrap 4's SASS files are compiled locally to produce the CSS files. You will most likely need to install SASS in your local machine.

`Django-assets` is used to manage the static assets. Any changes you make to the SASS files will be picked automatically as long as the development server is running.

To update the static assets after installing newer versions, run `npm run assets`

python manage.py collectstatic

#### Development
Set up the database credentials as appropriate, MySQL database is used.
Run local server: DJANGO_MODE=DEVELOPMENT python manage.py runserver

Run migrations, create a superuser account and start the development server.

DJANGO_MODE=DEVELOPMENT python manage.py migrate

### Testing
Tests make use of pytest through the pytest-django integration. All tests are located in the `tests` package.

