#!/bin/sh

# Compile sass
/bin/dart-sass/sass \
    data_models/static/data_models/sass/main.scss data_models/static/data_models/css/main.css


python scripts/check_database_connection.py

python manage.py migrate
python manage.py collectstatic --no-input

exec "$@"
