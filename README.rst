PyClass_API_Project
===================
####
Project Overview
####
An open source web app for visualizing word frequency of political statements over time using the Sunlight Foundation API. The application will feature user logins and saved searches.

####
Roster
####
Cam
  Skills: Databases, Backend, Minor HTML/CSS

Jade
  Skills: Backend, logic, text parsing, Selenium - browser automation

John
  Skills:

Jordan - Project Manager
  Skills: Front-End: HTML/CSS/Javascript. Python: Flask.

Nick
  Skills: Databases, Backend,

Chet
  Skills: Data management, Pandas

####
TODO
####
We know the project is finished when:
  A user can login, provide:
	  -search term
	  -date range
	  -boolean keywords or categories
  receives:
	  -graph
  can save:
	  -search

####
How to Install
####
Update pip_ and then setuptools

.. _pip: http://www.pip-installer.org/en/latest/installing.html

$ pip install --upgrade setuptools


create and activate the venv

open the main app directory

$ virtualenv .

$ source bin/activate


pip install the requirements

$ pip install -r requirements.txt --upgrade

If installation is a pain try this

$ pip install --allow-all-external --upgrade -r requirements.txt

If you are getting the error "ImportError: No module named setuptools" see this ImportError_ fix

.. _ImportError: https://github.com/pypa/pip/issues/1064


####
How to Setup the Database and Migrations
####

Alembic Migration Tutorial_

.. _Tutorial: http://blog.miguelgrinberg.com/post/flask-migrate-alembic-database-migration-wrapper-for-flask

cd to the src folder

To add migration support to your database you just need to run the init command:

$ python run.py db init

To issue your first migration you can run the following command:

$ python run.py db migrate

The next step is to apply the migration to the database. For this you use the upgrade command:

$ python run.py db upgrade

####
API Key
####

To run this app you must have an api key from sunlight academy.

Register: http://sunlightfoundation.com/api/accounts/register/

Create the file apikey.py under the src/ directory

Inside of the apikey.py file:

_API_KEY = '<your api key here>'

####
Mail Environment Variables
####

Export these variables to your environment so that the app can import sensitive information from the environment.

(venv) $ export MAIL_USERNAME=username

(venv) $ export MAIL_PASSWORD=password

(venv) $ export MAIL_ADMIN=email

Make sure there is no space between the '='

####
How to Run
####

#run the app

From the src folder:

$ python run.py runserver

go to http://127.0.0.1:5000/ or localhost:5000

####
How to test
####

From within the project root:

$ source bin/activate

$ cd src

$ python test.py

or the name of whatever test file you are running


To run selenium test:

From within the project root:

$ source bin/activate

$ python run.py

$ python test/selenium_test.py
