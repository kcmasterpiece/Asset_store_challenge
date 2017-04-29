# Planet Asset Store Coding Challenge

## by Jeff Fontas

This project uses the Django REST framework. I used python3 for development, and installed all dependencies in a virtualenv.  I assume that you have python3, virtualenv, and pip3 installed.

Here are instructions to run the application via manage.py:

1. Clone/copy the repo and cd into it
	cd Asset_store_challenge (or whatever the top level directory you cloned to is called)
2. Create virtual environment 
	virtualenv -p python3 env
3. Use virtualenv
	source env/bin/activate
4. Install dependencies
	pip install -r requirements.txt
5. Makemigrations and migrate
	python asset_store/manage.py makemigrations api
	python asset_store/manage.py migrate
6. Run the server
	python asset_store/manage.py runserver
7. Access the server on 127.0.0.1:8000/api 
