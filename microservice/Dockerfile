FROM python:3.9

WORKDIR /microservice

COPY ./requirements.txt /microservice/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /microservice/requirements.txt

COPY . /microservice/
