# Use the lightweight Alpine-based Python image
FROM python:3.9.13-alpine

# Set a working directory
WORKDIR /app

# Install required system dependencies
RUN apk add --no-cache curl

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python -

# Copy the local application code to the container
COPY . /app

# Set the PATH for poetry
ENV PATH="$PATH:/root/.local/bin"

# Install Python dependencies using Poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev

# Define the entrypoint for Gunicorn
ENTRYPOINT ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8000", "todo_app.app:create_app()"]
