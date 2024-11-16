# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Prevent Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevent Python from buffering stdout and stderr
ENV PYTHONUMBUFFERED 1

# Install netcat (using netcat-openbsd specifically) to wait for the database to be ready
RUN apt-get update && apt-get install -y netcat-openbsd

# Install pipenv globally
RUN pip install --no-cache-dir pipenv
# Copy Pipfile and Pipfile.lock into the container
COPY Pipfile Pipfile.lock ./
# Install dependencies using pipenv in system mode
RUN pipenv install --deploy --system

# Copy the entrypoint script into the container
COPY ./entrypoint.sh .
# Convert the entrypoint script to Unix format
RUN sed -i 's/\r$//g' /app/entrypoint.sh
# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Copy the entire project code into the container
COPY . .

# Run the entrypoint script
ENTRYPOINT [ "/app/entrypoint.sh" ]