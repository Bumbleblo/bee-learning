FROM python:3.7

WORKDIR /home

#RUN groupdadd -r tfx && useradd --no-log-init -r -g tfx tfx

RUN apt-get update && apt-get install -y \
    vim \
    tmux \
    && rm -rf /var/lib/apt/lists/*
    

ADD docker/requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
