# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables for Django
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE klimawatch.settings

# Create and set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Django application code into the container
COPY . /app/

# Run Django migrations
#RUN python manage.py migrate

# Collect statics
RUN python manage.py collectstatic --no-input

# Expose the port your Django app will run on
EXPOSE 8000

# runs the production server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "klimawatch.wsgi:application"]