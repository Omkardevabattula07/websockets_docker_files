# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
# Copy the Django project into the container
COPY . /app/

# Make the entrypoint.sh script executable
RUN chmod +x /app/entrypoint.sh

# Expose the port Django will run on
EXPOSE 8000

# Run the entrypoint.sh script
ENTRYPOINT ["/app/entrypoint.sh"]
