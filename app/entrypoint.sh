#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo "\nWaiting for the postgres service to be up and running\n"
python manage.py wait_for_db

echo "\nPreparing database migration files\n"
python manage.py makemigrations

echo "\nApplying the migration files to the database\n"
python manage.py migrate

exec "$@"