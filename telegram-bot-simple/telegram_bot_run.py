from flask.wrappers import Response
from flask import Flask
from flask import request, abort
from telegram_bot_api import (
    parse_message,
    send_message,
    deleteMessage,
    editMessageText,
    answerCallbackQuery,
)
from credentials import config
import asyncio
import json

token = config.TG_BOT_TOKEN

app = Flask(__name__)


def manage_messages(msg):
    parsed_message = parse_message(msg)
    if parsed_message:
        chat_id, message_info, chat_type = parsed_message
        if chat_type == "callback_query":
            handle_callback_query(chat_id, message_info)
        elif chat_type == "private message":
            handle_message(chat_id, message_info)


def handle_commands(message):
    reply = "Send /start to start the bot."
    inline_keyboard = ""
    if message == "/start":
        reply = "I reply and you can't do anything about it!"
    elif message == "🌈":
        reply = "🍹"
        inline_keyboard = {
            "inline_keyboard": [
                [{"text": "request", "callback_data": f"Clicked on request!"}],
            ]
        }
    elif message == "Clicked on request!":
        reply = "Request received!"
    return reply, inline_keyboard


def handle_message(chat_id, message_info):
    message, message_id = message_info
    reply, inline_keyboard = handle_commands(message)
    keyboard = [["/start", "🌈"]]
    reply_keyboard = {"keyboard": keyboard, "resize_keyboard": True}
    reply_markup = inline_keyboard if inline_keyboard else reply_keyboard
    r = asyncio.run(
        send_message(
            chat_id=chat_id,
            text=reply,
            reply_to_message_id=message_id,
            reply_markup=reply_markup,
        )
    )
    print("Sent response:", r)


def handle_callback_query(chat_id, message_info):
    (
        callback_query_id,
        message_id,
        callback_query_data,
        callback_query_message_id,
    ) = message_info
    command = callback_query_data
    reply, reply_markup = handle_commands(command)

    asyncio.run(answerCallbackQuery(callback_query_id, text="request is replied!"))
    r = asyncio.run(
        send_message(
            chat_id=chat_id,
            text=reply,
            reply_to_message_id=callback_query_message_id,
            reply_markup=reply_markup,
        )
    )
    print("Sent response:", r)


@app.route("/", methods=["POST"])
def index():
    message = request.get_json(force=True)
    print("Received message:", message)
    manage_messages(message)
    return Response("Ok", status=200)


def main():
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
