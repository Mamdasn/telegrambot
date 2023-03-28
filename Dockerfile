# syntax=docker/dockerfile:1

FROM python:3.11-alpine

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt

ENV TG_BOT_TOKEN="Run telegram-bot-setup.sh"

EXPOSE "Run telegram-bot-setup.sh"

CMD python3 telegram-bot-run.py &> /app/output/telegram-bot-run.log
