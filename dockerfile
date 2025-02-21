
FROM python:3.9


WORKDIR /app

COPY requirements.txt /app/

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for Flask
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Expose port 5000 for the Flask app
EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]

# to build and run the dockers
# docker build -t flask-user-api .
# docker run -p 5000:5000 flask-user-api
# docker tag flask-user-api balajiyoganantham/flask-api-usermanagement
#docker push balajiyoganantham/flask-api-usermanagement