#!/bin/sh

# Delete migrations
find . -path "*/migrations/*.py" -not -name "__init__.py" -not -path "./env"-delete
find . -path "*/migrations/*.pyc"  -delete
# Drop database
rm -rf ./db.sqlite3
. env/Scripts/activate
# pip install -r requirements.txt

# Create migrations and generate DB schema
./manage.py user-fixture
./manage.py runserver