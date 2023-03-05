# syntax=docker/dockerfile:1

FROM python:3.11-alpine

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt

ENV TG_BOT_TOKEN="Run telegram-bot-setup.sh"

EXPOSE 5000 5000

CMD ["python", "telegram-bot-run.py"]
