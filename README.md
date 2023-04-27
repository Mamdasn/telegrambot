# Telegram Bot
This repository contains a Python code that employs telegram bot api packaged as a Docker container. With this repo I want to facilitate access to the telegram bot api for people to provide services on it for others easier.

## Usage
First you should have access to a VPS. You can order it for cheap online. Then, to set up the bot, start by running the `telegram-bot-setup.sh` file. This script will configure a webhook on the Telegram servers to receive messages from the bot as soon as they are sent. The Dockerfile included in this repository has also been modified to include the HTTP API token for the Telegram bot.

To run the Telegram bot container, make sure you have already installed docker and docker-compose on your device. You can do so by entering this command in a terminal:

```bash
apt update -y
apt install docker docker-compose
```

Then, execute the following command: `sudo docker-compose up -d`. Docker-compose will spawn a docker container after the Dockerfile is built. There you go, now you should have a fully functional Telegram bot running in a docker container.

## Suggestions
Try to populate the telegram_bot_api library with other available methods and use them further on in the telegram-bot-run to improve user experience using your Telegram bot.   
