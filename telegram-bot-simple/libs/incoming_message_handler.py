import asyncio

from .telegram_bot_api import (  # deleteMessage,; editMessageText,
    answerCallbackQuery,
    parse_message,
    send_message,
    setMessageReaction,
)

# import json


def manage_messages(msg):
    """
    Processes incoming messages and dispatches them based on message type.

    This function acts as a router, directing messages to the appropriate handler
    based on whether it's a callback query or a private message.

    Args:
        msg (dict): A dictionary representing a message received from the Telegram API.
    """
    parsed_message = parse_message(msg)
    if parsed_message:
        chat_id, message_info, chat_type = parsed_message
        if chat_type == "callback_query":
            handle_callback_query(chat_id, message_info)
        elif chat_type == "private message":
            handle_message(chat_id, message_info)


def handle_commands(message):
    """
    Processes and responds to specific commands or inputs.

    Based on the input message, this function generates a reply and, if necessary, an
    inline keyboard structure for interactive responses in Telegram.

    Args:
        message (str): The text of the received message or command.

    Returns:
        tuple: A tuple containing the reply message (str) and the inline keyboard
               structure (dict) if applicable, otherwise an empty string.
    """
    reply = "Send /start to start the bot."
    inline_keyboard = ""
    if message == "/start":
        reply = "I reply and you can't do anything about it!"
    elif message == "🌈":
        reply = "🍹"
        inline_keyboard = {
            "inline_keyboard": [
                [{"text": "request", "callback_data": "Clicked on request!"}],
            ]
        }
    elif message == "Clicked on request!":
        reply = "Request received!"
    return reply, inline_keyboard


def handle_message(chat_id, message_info):
    """
    Handles a standard message received in a private chat.

    Extracts message content and ID from `message_info`, processes it through `handle_commands`,
    and then sends an appropriate response back to the user in the chat.

    Args:
        | chat_id (str): Unique identifier for the target chat.
        | message_info (tuple): A tuple containing the message text and message ID.

    Returns:
        None
    """
    message, message_id = message_info
    reply, inline_keyboard = handle_commands(message)
    keyboard = [["/start", "🌈"]]
    reply_keyboard = {"keyboard": keyboard, "resize_keyboard": True}
    reply_markup = inline_keyboard if inline_keyboard else reply_keyboard
    await asyncio.run(
        setMessageReaction(
            chat_id=chat_id,
            message_id=message_id,
            reaction={"type": "emoji", "emoji": "👍"},
        )
    )

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
    """
    Handles a callback query triggered by an inline keyboard in Telegram.

    Processes the callback query data, sends a notification of receipt, and responds with a message
    based on the content of the callback query.

    Args:
        | chat_id (str): Unique identifier for the target chat.
        | message_info (tuple): A tuple containing the callback query ID,
            the original message ID, the callback query data, and the callback query message ID.

    Returns:
        None
    """
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
