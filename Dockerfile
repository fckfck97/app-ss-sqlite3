# Pull base image
FROM python:3.11.1
ENV PYTHONUNBUFFERED 1
WORKDIR /app


# Install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy project
COPY . /app

CMD python manage.py runserver 0.0.0.0:8000