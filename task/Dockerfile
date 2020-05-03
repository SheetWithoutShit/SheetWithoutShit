FROM python:3.8.2

RUN mkdir /task

COPY requirements.txt /task

RUN pip install --upgrade pip && \
    pip install -r /task/requirements.txt
