# User-Management-App-of-Apps
A Django application that enables user management for multiple apps, provides rest API for client communication.

Project uses uv
## Commands 

```bash
// Create the main app
uv run django-admin startproject app .


// add an app within the main app

uv run manage.py startapp ${new_app_within_main}

// add new app to INSTALLED_APPS located in app/settings.py 

// how run migration for new app

uv run manage.py makemigrations ${new_app_within_main}

uv run manage.py migrate

// To run application
uv run manage.py runserver




```