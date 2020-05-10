FROM python:3.8.2

RUN mkdir /tasker

COPY requirements.txt /tasker

RUN pip install --upgrade pip && \
    pip install -r /tasker/requirements.txt

WORKDIR /tasker/app
