import os
import sys
from flask import Flask, abort, request

from serializer import validate_registration_params, UnValidError, is_valid_token
from registration_starter import start_registration
from logger import get_logger


app = Flask(__name__)

logger = get_logger()


@app.route("/", methods=["POST"])
def root():
    if not is_valid_token(app.config["SLACK_APP_TOKEN"], request.form["token"]):
        abort(403)
    try:
        url_or_text, emoji_name, response_url = validate_registration_params(request.form)
    except UnValidError as e:
        logger.error(e.message)
        abort(400, e.message)

    start_registration(url_or_text, emoji_name, response_url)

    return "Registering %s ...." % emoji_name


def _run_server():
    error_messages = []
    if not os.environ.get("SLACK_APP_TOKEN"):
        error_messages.append("Please set SLACK_APP_TOKEN to env val.")
    if not os.environ.get("PORT"):
        error_messages.append("Please set PORT to env val.")
    if len(error_messages) > 0:
        for message in error_messages:
            logger.error(message)
        sys.exit(1)

    app.config["SLACK_APP_TOKEN"] = os.environ["SLACK_APP_TOKEN"]
    app.run(host="0.0.0.0", port=int(os.environ["PORT"]))


if __name__ == "__main__":
    _run_server()
