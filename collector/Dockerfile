FROM python:3.8.2

RUN mkdir /collector

WORKDIR /collector

RUN echo ls

COPY requirements.txt /collector

RUN pip install --upgrade pip && \
    pip install -r requirements.txt
