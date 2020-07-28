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
echo "\nPostgres database service is now up and running"

echo "\nPreparing database migration files\n"
python manage.py makemigrations
echo "\nMigration files generated successfully"

echo "\nApplying the migration files to the database\n"
python manage.py migrate
echo "\nMigrations applied to the database successfully"

echo "\nCollecting the static files"
python manage.py collectstatic --no-input
echo "\nStatic files collect successfully"
echo "\nBooting up the development server ...\n"

exec "$@"