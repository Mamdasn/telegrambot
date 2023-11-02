from flask.wrappers import Response
from flask import Flask
from flask import request, abort
from telegram_bot_api import parse_message, \
                                send_message, \
                                deleteMessage, \
                                editMessageText
from credentials import config
import json

token = config.TG_BOT_TOKEN

app = Flask(__name__)

def manage_messages(msg):
    parsed_message = parse_message(msg)
    if parsed_message:
        chat_id, message_info, chat_type = parsed_message
        if chat_type == 'private message':
            handle_message(chat_id, message_info)
        
def handle_commands(message):
    reply = 'send /start to start the bot.'
    if message == '/start':
        reply = 'Hello!'
    return reply
    
def handle_message(chat_id, message_info):
    message, message_id = message_info
    reply = handle_commands(message) 
    keyboard = [["/start"]]
    reply_markup = {"keyboard": keyboard, "resize_keyboard": True}
    r = send_message(
            chat_id=chat_id, 
            text=reply,
            reply_to_message_id=message_id,
            reply_markup=reply_markup
            )
    print('Sent response:', r)
    
@app.route('/', methods=['POST'])
def index():
    message = request.get_json(force=True)
    print('Received message:', message)
    manage_messages(message)
    return Response('Ok', status=200)

def main():
    pass
 

if __name__ == "__main__": 


    app.run(host="0.0.0.0", port=5000)

