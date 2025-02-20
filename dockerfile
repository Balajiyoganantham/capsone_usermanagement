# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file first for caching dependencies
COPY requirements.txt /app/

# Copy the rest of the application code into the container
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for Flask
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Expose port 5000 for the Flask app
EXPOSE 5000

# Define command to run the application
CMD ["flask", "run", "--host=0.0.0.0"]
