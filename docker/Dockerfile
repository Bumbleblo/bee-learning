FROM python:3.6-alpine

WORKDIR /home

ADD docker/requirements.txt .

RUN apk add build-base

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]
