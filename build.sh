#!/usr/bin/env bash
set -o errexit  # Exit on error

# Install dependencies
pip install -r requirements.txt

# Run Django management commands
python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate
