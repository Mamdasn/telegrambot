import asyncio
from random import choice as pick_randomly

from .telegram_bot_api import (  # deleteMessage,; editMessageText,; setMessageReaction,
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
        elif chat_type in ("private", "group", "supergroup"):
            handle_message(chat_id, message_info, chat_type)


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


def handle_message(chat_id, message_info, chat_type="private"):
    """
    Handles a standard message received in a private chat.

    Extracts message content and ID from `message_info`, processes it through `handle_commands`,
    and then sends an appropriate response back to the user in the chat.

    :param chat_id: Unique identifier for the target chat or username of the target channel.
    :type chat_id: int
    :param message_info: Tuple containing the message text and message ID.
    :type message_info: tuple
    :param chat_type: Type of the chat, defaults to "private". Can also be "group".
    :type chat_type: str, optional

    :return: None. The function sends messages and handles responses asynchronously.
    :rtype: NoneType

    Note:
        In group chats, the function only processes messages that start with "/" (commands).
    """
    message, message_id, _ = message_info

    if not message:
        return

    # Commands explicitly meant for bots in groups (e.g., /command@bot_username).
    if chat_type in ("group", "supergroup"):
        if "@" not in message:
            return
        else:
            message = message[: message.rfind("@")]

    reply, inline_keyboard = handle_commands(message)

    emojies = [
        "👍",
        "👎",
        "❤",
        "🔥",
        "🥰",
        "👏",
        "😁",
        "🤔",
        "🤯",
        "😱",
        "🤬",
        "😢",
        "🎉",
        "🤩",
        "🤮",
        "💩",
        "🙏",
        "👌",
        "🕊",
        "🤡",
        "🥱",
        "🥴",
        "😍",
        "🐳",
        "❤‍🔥",
        "🌚",
        "🌭",
        "💯",
        "🤣",
        "⚡",
        "🍌",
        "🏆",
        "💔",
        "🤨",
        "😐",
        "🍓",
        "🍾",
        "💋",
        "🖕",
        "😈",
        "😴",
        "😭",
        "🤓",
        "👻",
        "👨‍💻",
        "👀",
        "🎃",
        "🙈",
        "😇",
        "😨",
        "🤝",
        "✍",
        "🤗",
        "🫡",
        "🎅",
        "🎄",
        "☃",
        "💅",
        "🤪",
        "🗿",
        "🆒",
        "💘",
        "🙉",
        "🦄",
        "😘",
        "💊",
        "🙊",
        "😎",
        "👾",
        "🤷‍♂",
        "🤷",
        "🤷‍♀",
        "😡",
    ]
    reaction = [{"type": "emoji", "emoji": pick_randomly(emojies)}]
    is_big = True
    r = asyncio.run(setMessageReaction(chat_id, message_id, reaction, is_big))
    print("React response:", r)

    keyboard = [
        [{"text": "/start"}, {"text": "🌈"}],
        [
            {
                "text": "Source Code 📟",
                "web_app": {"url": "https://github.com/Mamdasn/telegrambot"},
            }
        ],
    ]

    reply_keyboard = {"keyboard": keyboard, "resize_keyboard": True}
    reply_markup = inline_keyboard if inline_keyboard else reply_keyboard

    if chat_type in ("group", "supergroup"):
        reply_markup = None

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
