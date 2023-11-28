# Telegram Bot
This repository contains a Python code that employs telegram bot api packaged as a Docker container. With this repo I want to facilitate access to the telegram bot api for people to provide services on it for others easier.

## Usage
First you should have access to a VPS. You can order it for cheap online. Make sure to export the environmental variables `IP_ADDRESS` and `TG_BOT_TOKEN`. Then, to set up and run the bot, start by running the command `docker compose up --build -d`. Note that within the Dockerfile at first a pair of SSL files are created then configured with the telegram webhook on the Telegram servers to receive messages from the bot as soon as they are sent.

To run the Telegram bot container, make sure you have already installed docker and docker-compose on your device. There you go, now you should have a fully functional Telegram bot running in a docker container.

## Documentation
The documentation can be found [HERE](https://mamdasn.github.io/telegrambot/)
