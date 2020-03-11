FROM python:3.7.6-alpine3.11

WORKDIR /home

RUN apk add --update \
    gcc \
    g++ \
    linux-headers

RUN pip3 install apache-airflow
