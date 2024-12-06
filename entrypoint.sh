#!/bin/sh

if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for PostgreSQL to start..."

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi

# Run database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Execute the container's main process (CMD)
exec "$@"
