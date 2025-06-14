#!/usr/bin/env bash

# Wait until the database is ready
echo "Waiting for Postgres to be available..."
while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
  sleep 1
done

echo "Postgres is available, continuing..."
#!/usr/bin/env bash

echo "🛠 Installing dependencies..."
pip install -r requirements.txt

echo "🧹 Collecting static files..."
python manage.py collectstatic --noinput

echo "📦 Making migrations..."
python manage.py makemigrations --noinput

echo "🚀 Applying migrations..."
python manage.py migrate --noinput


# Run migrations
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
