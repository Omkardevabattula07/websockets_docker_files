#!/bin/bash

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done
echo "PostgreSQL started"

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create a superuser
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(os.getenv('DJANGO_SUPERUSER_USERNAME'), os.getenv('DJANGO_SUPERUSER_EMAIL'), os.getenv('DJANGO_SUPERUSER_PASSWORD')) if not User.objects.filter(username=os.getenv('DJANGO_SUPERUSER_USERNAME')).exists() else print('Superuser already exists')" | python manage.py shell

# Start the Django development server
python manage.py runserver 0.0.0.0:8000
