# Use the official Python 3.10 slim image from the Docker Hub
FROM python:3.10-slim

# Set environment variables to prevent Python from writing .pyc files to disk and to buffer stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=False
ENV DEPLOYMENT=False

# Install Poetry
RUN pip install poetry

# Create and set the working directory
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files to the working directory
COPY pyproject.toml poetry.lock ./

# Install the project dependencies
RUN poetry install --no-root

# Copy the entire project to the working directory
COPY . .

# Run Django commands to prepare the application
RUN poetry run python manage.py collectstatic --noinput

# Apply database migrations
RUN poetry run python manage.py migrate

# Expose the port that the Django app runs on
EXPOSE 8000

# Define the command to run the Django server
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
