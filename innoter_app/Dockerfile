FROM python:3.9.6-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /innoter_app
COPY requirements.txt /innoter_app/
RUN pip install -r requirements.txt
COPY . /innoter_app/
