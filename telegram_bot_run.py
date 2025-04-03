from flask import Flask, abort, request
from flask.wrappers import Response

import libs.incoming_message_handler as incoming_message_handler

app = Flask(__name__)


@app.before_request
def abortion_method():
    # use the ip for future patches
    ip = str(request.environ.get("HTTP_X_REAL_IP", request.remote_addr))
    print(ip)
    if (request.method == "GET") or (request.args != {}):
        abort(403)


@app.route("/", methods=["POST"])
def index():
    received_message = request.get_json(force=True)
    incoming_message_handler.manage_messages(received_message)
    return Response("Ok", status=200)


def main():
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
