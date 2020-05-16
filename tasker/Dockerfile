FROM python:3.8.2

RUN apt-get update && apt-get -y install cron

ENV TZ=Europe/Kiev
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY cronjobs /etc/cron.d/tasker_cronjobs
RUN chmod 0644 /etc/cron.d/tasker_cronjobs && \
    crontab /etc/cron.d/tasker_cronjobs

RUN mkdir /tasker

COPY requirements.txt /tasker
RUN pip install --upgrade pip && \
    pip install -r /tasker/requirements.txt

WORKDIR /tasker/app
