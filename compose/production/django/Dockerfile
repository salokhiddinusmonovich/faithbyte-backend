# Use the official Python image from the Docker Hub
ARG PYTHON_VERSION=3.10-slim-bullseye

# Define the Python base image
FROM python:${PYTHON_VERSION} as python

# Build Stage
FROM python as python-build-stage

# Install build dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and build dependency wheels
COPY ./requirements /requirements
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r /requirements/requirements.txt

# Final Stage
FROM python as python-run-stage

# Define the app's home directory
ARG APP_HOME=/app
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR ${APP_HOME}

# Install runtime dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy prebuilt wheels and install dependencies
COPY --from=python-build-stage /wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/*

# Copy application code
COPY . ${APP_HOME}

# Create and use a non-root user for security
RUN addgroup --system django && adduser --system --ingroup django django
RUN chown -R django:django ${APP_HOME}
USER django

# Expose the port Django will run on
EXPOSE 8000

# Copy the entrypoint script from the Django directory to the root of the container
COPY ./django/entrypoint /entrypoint

# Make sure the entrypoint script is executable
RUN chmod +x /entrypoint

# Set the entrypoint to use the entrypoint script
ENTRYPOINT ["/entrypoint"]

# The command to run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
