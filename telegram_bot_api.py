import requests
from credentials import config

token = config.TG_BOT_TOKEN
base_link = f'https://api.telegram.org/bot{token}'

class Message:
    def __init__(self, message: dict):
        self._message = message
    def __getitem__(self, key):
        keys = key if isinstance(key, tuple) else (key,)
        message = self._message
        for k in keys:
            if not isinstance(message, dict): return None
            message = message.get(k)
        return message 

def parse_message(msg):
    """
    Parses a message object received from the Telegram API.

    Args:
        msg (dict): A dictionary representing a Telegram message.

    Returns:
        chat_id (int): The ID of the chat the message was sent in.
        message_info (list): A list containing information about the message.
        message_type (str): 'message'.
    """
    msg = Message(msg)
    message   = msg['message']
    chat      = msg['message', 'chat']
    chat_id   = msg['message', 'chat', 'id']
    chat_type = msg['message', 'chat', 'type']
    if chat_type == 'private': 
        message_id = msg['message', 'message_id']
        txt        = msg['message', 'text']
        message_info = [txt, message_id]
        return chat_id, message_info, 'message'
    
def sendChatAction(chat_id, action='typing'): 
    """
    Parameters:
    ----------
    chat_id (str):
        Unique identifier for the target chat or username of the target channel
    action (str):
        Type of action to broadcast. Choose one, depending on what the user is about to receive: typing for text messages, upload_photo for photos, record_video or upload_video for videos, record_voice or upload_voice for voice notes, upload_document for general files, choose_sticker for stickers, find_location for location data, record_video_note or upload_video_note for video notes.
    ----------
    Return:
        Request response
    """
    url = f"{base_link}/sendChatAction"
    payload = {'chat_id': chat_id, 'action': action}
    r = requests.post(url, json=payload)
    return r

def send_message(chat_id, text, reply_to_message_id=None, reply_markup=None):
    """
    Parameters:
    ----------
    chat_id (str):
        Unique identifier for the target chat or username of the target channel
    reply_to_message_id (str):
        If the message is a reply, ID of the original message
    reply_markup (str):
        Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
    ----------
    Return:
        Request response
    """
    sendChatAction(chat_id, action='typing')
    url = f"{base_link}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = reply_markup
    r = requests.post(url, json=payload)
    return r

def deleteMessage(chat_id, message_id):
    """
    Parameters:
    ----------
    chat_id (str):
        Unique identifier for the target chat or username of the target channel
    message_id (str):
        Identifier of the message to delete
    ----------
    Return:
        Request response
    """
    url = f"{base_link}/deleteMessage"
    payload = {'chat_id': chat_id, 'message_id': message_id}
    r = requests.post(url, json=payload)
    return r

def editMessageText(chat_id, message_id, text, reply_markup=None):
    """
    Parameters:
    ----------
    chat_id (str):
        Unique identifier for the target chat or username of the target channel
    message_id (str):
        Required if inline_message_id is not specified. Identifier of the message to edit
    ----------
    Return:
        Request response
    """
    sendChatAction(chat_id, action='typing')
    url = f"{base_link}/editMessageText"
    payload = {'chat_id': chat_id, 'message_id': message_id, 'text': text, 'parse_mode': 'HTML'}
    if reply_markup:
        payload['reply_markup'] = reply_markup
    r = requests.post(url, json=payload)
    return r
