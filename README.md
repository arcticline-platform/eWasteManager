# eWasteManager is a service for managing electronic waste. 
** A collection agency/agent sets up an account to start a collection service in his or her locality. Users must then subscribe to the agents account to call the service when needed. In monetisation, the agents subscribe for service to set an account and they(agents) can will also be able to collect money from or pay their subscribers.

** The application is developed in Python using Django Framework with HTML5, CCS3 and Javascript for the frontend.The application is location based with geospatial data for locating users. GeoDjango has been used for this purpose. <a href="https://docs.djangoproject.com/en/4.2/ref/contrib/gis/tutorial/#introduction">Read documentation</a>

** Its follows PEP8 code formating style and code reusability with Object Oriented programming is encouraged.
-------------------------------------------------------------------------------------------------------------
# Setup of the Apllication
# Requirements
** Python 3.7 and above

** Django 3.2

** PostgreSQL 13 and above with POSTGIS installed
----------------------------------------------------------
# Installation
1. git clone repo
2. Install <a href="https://www.postgresql.org/download/">PostgresSQL</a> and setup a database
3. Install Geospatial libraries according the Django Documentation <a href="https://docs.djangoproject.com/en/4.2/ref/contrib/gis/install/geolibs/">avaialable here</a>
4. Python -m venv <virtual-environment-name>
5. Pip install -r requirements.txt
----------------------------------------------------------
# Running the application
** Create .env file with corresponding values from .env_example

** python manage.py makemigrations // When there is a new update on the model(s)

** python manage.py migrate

** Python manage.py runserver