FROM python:3.8.2

RUN mkdir /telegram

COPY requirements.txt /telegram

RUN pip install --upgrade pip && \
    pip install -r /telegram/requirements.txt
