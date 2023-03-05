# Telegram Bot
This repository contains a Python code that employs telegram bot api packaged as a Docker container. With this repo I want to facilitate access to the telegram bot api for people to provide services on it for others easier.

## Usage
To set up the bot, start by running the `telegram-bot-setup.sh` file. This script will configure a webhook on the Telegram servers to receive messages from the bot as soon as they are sent. The Dockerfile included in this repository has also been modified to include the HTTP API token for the Telegram bot.

To run the Telegram bot container, execute the following command: `sudo docker-compose up -d`.
