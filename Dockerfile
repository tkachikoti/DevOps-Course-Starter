# Stage 1: Base image with common operations and dependencies
FROM python:3.9.13-alpine as base

# Set a working directory
WORKDIR /app

# Install required system dependencies
RUN apk add --no-cache curl

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python -

# Copy the rest of the local application code to the container
COPY . /app

# Set the PATH for poetry
ENV PATH="$PATH:/root/.local/bin"

# Install Python dependencies using Poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev

# Stage 2: Production image
FROM base as production

# Define the entrypoint for Gunicorn
ENTRYPOINT ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8000", "todo_app.app:create_app()"]

# Stage 3: Development image
FROM base as development

# Expose the Flask application port
EXPOSE 5000

# Set the FLASK_APP environment variable
ENV FLASK_APP=todo_app/app.py

# Set the entrypoint for development
CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0", "--reload"]
