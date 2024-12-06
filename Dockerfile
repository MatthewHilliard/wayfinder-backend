# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Prevent Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install netcat for database readiness checks
RUN apt-get update && apt-get install -y netcat-openbsd

# Install pipenv globally
RUN pip install --no-cache-dir pipenv

# Copy Pipfile and Pipfile.lock into the container
COPY Pipfile Pipfile.lock ./

# Install dependencies using pipenv in system mode
RUN pipenv install --deploy --system

# Copy the entire project code into the container
COPY . .

# Set up static files (for production)
RUN python manage.py collectstatic --noinput

# Run Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wayfinder.wsgi:application"]
