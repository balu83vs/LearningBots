FROM python:3.10

WORKDIR /home

ENV TELEGRAM_API_TOKEN="6083034488:AAHXKRr0GRgHG7sZ8_e9guaMi0wjDCh85Wk"
ENV TELEGRAM_ACCESS_ID="506101077"
#ENV TELEGRAM_PROXY_URL=""
#ENV TELEGRAM_PROXY_LOGIN=""
#ENV TELEGRAM_PROXY_PASSWORD=""

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install -U pip aiogram pytz && apt-get update && apt-get install sqlite3
COPY *.py ./
COPY createdb.sql ./
RUN sqlite3 finance.db < createdb.sql

ENTRYPOINT ["python", "server.py"]

