# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Эта переменная окружения устанавливает флаг для интерпретатора Python, чтобы не создавать .pyc файлы (компилированные файлы байткода) при выполнении Python-скриптов
ENV PYTHONDONTWRITEBYTECODE=1
# Когда флаг установлен в 1, вывод Python не будет буферизоваться, и данные будут сразу же выводиться на стандартные потоки вывода (например, на терминал или в лог-файл)
ENV PYTHONUNBUFFERED=1

WORKDIR /kitchen_app

COPY ./app/reqs.txt ./app/
RUN cd app && pip install -r reqs.txt

COPY ./conf ./conf
COPY ./deploy-to-server.sh .
COPY ./entrypoint.sh .
COPY ./run-celery.sh .
COPY ./run-sheduler.sh .
COPY ./.env .

COPY ./app ./app

