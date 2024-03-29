from flask import Flask, request
from flask.wrappers import Response
from libs.incoming_message_handler import manage_messages

app = Flask(__name__)


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
