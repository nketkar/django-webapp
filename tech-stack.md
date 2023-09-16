## An overview of the technology stack used

### Database
`MySQL, v 5.7.20`

Connection with python is done using the `mysqlcient` DB adapter, version 1.13.12

### Backend
The app runs on `Django 1.11.7`, which runs on `Python 2.7.12`

Several python packages are used in this project:
0. `django-geoposition` - used to make interaction with google maps easy in Django.
1. `tablib` - generating CSV and Excel datasets.
2. `django-crispy-forms` - rendering forms with bootstrap
3. `django-assets` - front end assets maangement in django templates.
4. `django-argonauts` - safely generate generate json data in django templates
     for use in javascript scripts.
5. `pytest` - for tests.
6. `django-registration` - for HMAC based user registration.
7. `django-honeypot` - to prevent automated form spam.

Kindly refer to the requirements.txt file for details.

All these packages are installed in a virtual environment. The virtual environment is managed used `virtualenvwrapper`. However, virtualenvwrapper is installed globally, version 4.8.2.

### Front end
#### Bootstrap
`Bootstrap 4` is used. Specifically, Bootstrap 4 SASS files are compiled locally
to generate the css by django-assets. Under the hood, django-assets uses the ruby gem sass.
For this reason, Ruby and the sass gem should be installed.

The server uses` Ruby 2.3.1` and `sass 3.5.3`

#### NodeJS
NodeJS is used in front end asset management: installing, upgrading and copying of the required JS libraries.

`Node 9.2.0` and `npm 5.6.0` are used.

Kindly refer to the `package.json` file.

`UglifyJS`, an npm package, is used to minify and uglify the js files before
rendering in production. It's installed globally.
