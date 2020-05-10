FROM python:3.8.2

RUN mkdir /server

COPY requirements.txt /server

RUN pip install --upgrade pip && \
    pip install -r /server/requirements.txt

WORKDIR /server/app
