FROM python:3.8.2

RUN mkdir /collector

COPY requirements.txt /collector

RUN pip install --upgrade pip && \
    pip install -r /collector/requirements.txt

WORKDIR /collector/app
