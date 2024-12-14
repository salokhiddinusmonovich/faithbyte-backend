# Use the official Python image from the Docker Hub
ARG PYTHON_VERSION=3.10-slim-bullseye

# Define the Python base image
FROM python:${PYTHON_VERSION} as python

# Build Stage
FROM python as python-build-stage

ARG BUILD_ENVIRONMENT=production


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

ARG BUILD_ENVIRONMENT=production
ARG APP_HOME=/app



ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

# Define the app's home directory
ARG APP_HOME=/app
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR ${APP_HOME}

# Install dependencies for GDAL and PostGIS
RUN apt-get update && apt-get install -y \
    libgdal-dev \
    postgis \
    && rm -rf /var/lib/apt/lists/*

# Ensure GDAL is available
ENV GDAL_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/libgdal.so

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
# Copy the entrypoint script and set ownership
COPY --chown=django:django ./compose/production/django/entrypoint /entrypoint
RUN chmod +x /entrypoint

# Temporarily change ownership to root to modify the file, then reset back to django
USER root
RUN sed -i 's/\r$//g' /entrypoint
USER django

# Copy the start script and set ownership
COPY --chown=django:django ./compose/production/django/start /start
RUN chmod +x /start

# Temporarily change ownership to root to modify the file, then reset back to django
USER root
RUN sed -i 's/\r$//g' /start
USER django


# Expose the port Django will run on
EXPOSE 8000
RUN pip install gunicorn


# Set the entrypoint to use the entrypoint script
ENTRYPOINT ["/entrypoint"]

# The command to run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
