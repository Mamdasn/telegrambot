import aiohttp
import asyncio
from credentials import config

token = config.TG_BOT_TOKEN
base_link = f"https://api.telegram.org/bot{token}"


class Message:
    """
    A class to represent and process a message object.

    This class provides methods to extract various pieces of information from
    a message dictionary, typically received from an API like Telegram.

    Attributes:
        _message (dict): The original message dictionary.

    Methods:
        message: Retrieves the main message content.
        chat: Retrieves chat information from the message.
        chat_id: Retrieves the unique chat ID.
        chat_type: Retrieves the type of chat (e.g., private, group).
        message_id: Retrieves the ID of the message.
        message_text: Retrieves the text of the message.
        message_info: Retrieves a tuple with text and ID of the message.
        callback_query: Retrieves callback query information.
        callback_query_id: Retrieves the callback query ID.
        callback_query_data: Retrieves the callback query data.
        callback_query_message: Retrieves the message related to the callback query.
        callback_query_message_id: Retrieves the message ID of the callback query.
        callback_query_message_chat: Retrieves chat information of the callback query message.
        callback_query_message_chat_id: Retrieves the chat ID of the callback query message.
        callback_query_reply_to_message: Retrieves the original message to which the callback query is replying.
        callback_query_reply_to_message_message_id: Retrieves the message ID of the original message in the callback query.
        callback_query_message_info: Retrieves a tuple with detailed info of the callback query message.
    """
    def __init__(self, message: dict):
        """
        Initializes the Message object with a message dictionary.

        Args:
            message (dict): A dictionary representing a message.
        """
        self._message = message

    @staticmethod
    def _getitem(dic, key):
        keys = key if isinstance(key, tuple) else (key,)
        query = dic
        for k in keys:
            if not isinstance(query, dict):
                return None
            query = query.get(k)
        return query

    @property
    def message(self):
        return self._getitem(self._message, "message")

    @property
    def chat(self):
        return self._getitem(self.message, "chat")

    @property
    def chat_id(self):
        return self._getitem(self.message, ("chat", "id"))

    @property
    def chat_type(self):
        return self._getitem(self.message, ("chat", "type"))

    @property
    def message_id(self):
        if self.chat_type == "private":
            return self._getitem(self.message, "message_id")

    @property
    def message_text(self):
        if self.chat_type == "private":
            return self._getitem(self.message, "text")

    @property
    def message_info(self):
        return (self.message_text, self.message_id)

    @property
    def callback_query(self):
        return self._getitem(self._message, "callback_query")

    @property
    def callback_query_id(self):
        return self._getitem(self.callback_query, "id")

    @property
    def callback_query_data(self):
        return self._getitem(self.callback_query, "data")

    @property
    def callback_query_message(self):
        return self._getitem(self.callback_query, "message")

    @property
    def callback_query_message_id(self):
        return self._getitem(self.callback_query_message, "message_id")

    @property
    def callback_query_message_chat(self):
        return self._getitem(self.callback_query_message, "chat")

    @property
    def callback_query_message_chat_id(self):
        return self._getitem(self.callback_query_message_chat, "id")

    @property
    def callback_query_reply_to_message(self):
        return self._getitem(self.callback_query_message, "reply_to_message")

    @property
    def callback_query_reply_to_message_message_id(self):
        return self._getitem(self.callback_query_reply_to_message, "message_id")

    @property
    def callback_query_message_info(self):
        return (
            self.callback_query_id,
            self.callback_query_reply_to_message_message_id,
            self.callback_query_data,
            self.callback_query_message_id,
        )


def parse_message(msg):
    """
    Parses a message object received from the Telegram API.

    Analyzes the message to extract various components like chat ID and message information. Differentiates between normal messages and callback queries.

    Args:
        msg (dict): A dictionary representing a Telegram message.

    Returns:
        tuple: A tuple containing the chat ID, message information, and message type.
    """
    msg = Message(msg)
    if msg.callback_query:
        return (
            msg.callback_query_message_chat_id,
            msg.callback_query_message_info,
            "callback_query",
        )
    elif msg.chat_type == "private":
        return msg.chat_id, msg.message_info, "private message"


async def post_json(url, json_data):
    """
    Asynchronously sends a POST request with JSON data.

    This function is a utility to send asynchronous POST requests to a specified URL with JSON-formatted data.

    Args:
        url (str): The URL to which the request is to be sent.
        json_data (dict): The JSON data to be sent in the POST request.

    Returns:
        str: The text response of the request.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=json_data) as response:
            return await response.text()


async def sendChatAction(chat_id, action="typing"):
    """
    Asynchronously sends a chat action to a Telegram chat.

    This function is used to send various chat actions to inform users in a chat about the ongoing activity (e.g., typing, uploading a photo).

    Args:
        chat_id (str): Unique identifier for the target chat or username of the target channel.
        action (str): Type of action to broadcast (e.g., 'typing', 'upload_photo').

    Returns:
        str: The text response of the request.
    """
    url = f"{base_link}/sendChatAction"
    payload = {"chat_id": chat_id, "action": action}
    r = asyncio.create_task(post_json(url, payload))
    return await r


async def send_message(chat_id, text, reply_to_message_id=None, reply_markup=None):
    """
    Asynchronously sends a message to a Telegram chat.

    This function allows sending a text message to a specified chat in Telegram. Additional parameters allow specifying a reply and custom keyboards.

    Args:
        chat_id (str): Unique identifier for the target chat or username of the target channel.
        text (str): The text of the message to be sent.
        reply_to_message_id (str, optional): If the message is a reply, ID of the original message.
        reply_markup (str, optional): Additional interface options in JSON-serialized format.

    Returns:
        str: The text response of the request.
    """

    await asyncio.create_task(sendChatAction(chat_id, action="typing"))
    url = f"{base_link}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if reply_to_message_id:
        payload["reply_to_message_id"] = reply_to_message_id
    if reply_markup:
        payload["reply_markup"] = reply_markup
    r = asyncio.create_task(post_json(url, payload))
    return await r


async def deleteMessage(chat_id, message_id):
    """
    Asynchronously deletes a message from a Telegram chat.

    This function is used to delete a message in a Telegram chat based on its unique message ID.

    Args:
        chat_id (str): Unique identifier for the target chat or username of the target channel.
        message_id (str): Identifier of the message to delete.

    Returns:
        str: The text response of the request.
    """
    url = f"{base_link}/deleteMessage"
    payload = {"chat_id": chat_id, "message_id": message_id}
    r = asyncio.create_task(post_json(url, payload))
    return await r


async def editMessageText(chat_id, message_id, text, reply_markup=None):
    """
    Asynchronously edits the text of a message in a Telegram chat.

    This function allows editing the text of an existing message in a Telegram chat. It requires the message ID and the new text. Optionally, it can also update the reply markup.

    Args:
        chat_id (str): Unique identifier for the target chat or username of the target channel.
        message_id (str): Identifier of the message to edit.
        text (str): New text to replace the existing message content.
        reply_markup (str, optional): Additional interface options in JSON-serialized format.

    Returns:
        str: The text response of the request.
    """

    await asyncio.create_task(sendChatAction(chat_id, action="typing"))
    url = f"{base_link}/editMessageText"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "HTML",
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    r = asyncio.create_task(post_json(url, payload))
    return await r


async def answerCallbackQuery(callback_query_id, text):
    """
    Asynchronously sends a response to a callback query in Telegram.

    This function is used to provide feedback to a user who initiated a callback query in a Telegram bot interaction.

    Args:
        callback_query_id (str): Unique identifier for the callback query.
        text (str): Text of the notification to be shown to the user.

    Returns:
        str: The text response of the request.
    """
    url = f"{base_link}/answerCallbackQuery"
    payload = {"callback_query_id": callback_query_id, "text": text}
    r = asyncio.create_task(post_json(url, payload))
    return await r
