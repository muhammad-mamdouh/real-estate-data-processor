#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo "\nPreparing database migration files\n"
python manage.py makemigrations

echo "\nApplying the migration files to the database\n"
python manage.py migrate

exec "$@"