# Stage 1: Base image with common operations and dependencies
FROM python:3.9.13-alpine as base

# Set a working directory
WORKDIR /app

# Install required system dependencies
RUN apk add --no-cache curl

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python -

# Set the PATH for poetry
ENV PATH="$PATH:/root/.local/bin"

# Disable virtualenv creation
RUN poetry config virtualenvs.create false && \
    poetry config virtualenvs.in-project false

# Copy the rest of the local application code to the container
COPY . /app


# Stage 2: Production image
FROM base as production

# Install Python dependencies using Poetry
 RUN poetry install --no-dev

# Define the entrypoint for Gunicorn
CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:$PORT", "todo_app.app:create_app()"]


# Stage 3: Development image
FROM base as development

# Install Python dependencies using Poetry
 RUN poetry install

# Expose the Flask application port
EXPOSE 5000

# Set the FLASK_APP environment variable
ENV FLASK_APP=todo_app/app.py

# Set the command for development
CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0", "--reload"]


# Stage 4: Debug image
FROM base as debug

# Install Python dependencies using Poetry
 RUN poetry install

# Expose the Flask application port
EXPOSE 5000

# Set the FLASK_APP environment variable
ENV FLASK_APP=todo_app/app.py

# Set the environment to development
ENV FLASK_ENV=development

# Keep the container running
CMD tail -f /dev/null


# Stage 4: Test environment
FROM base as test

# Copy your application code and tests
COPY . /app

# Install dependencies
RUN poetry install

# Run tests
ENTRYPOINT ["poetry", "run", "pytest"]
