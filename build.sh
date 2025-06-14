#!/usr/bin/env bash

# Wait until the database is ready
echo "Waiting for Postgres to be available..."
while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
  sleep 1
done

echo "Postgres is available, continuing..."

# Run migrations
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
