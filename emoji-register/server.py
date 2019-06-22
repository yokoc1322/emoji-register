import os
import re
import sys
import json
import logging
from multiprocessing import Process

import requests
from flask import Flask, request, abort
from emoji import register_emoji, register_moji

LOGGER_NAME = "emoji_register"

app = Flask(__name__)

RE_URL = re.compile(r"^(http|https)://([-\w]+\.)+[-\w]+(/[-+\w./?%&=]*)?$")


def _is_text_url(text):
    if RE_URL.match(text):
        return True
    return False


def _register_moji_with_delay_return(response_url, emoji_text, emoji_name):
    return_text = register_moji(emoji_text, emoji_name)
    headers = {"content-type": "application/json"}
    data = {"text": return_text}
    r = requests.post(response_url, data=json.dumps(data), headers=headers)

    logger = logging.getLogger(LOGGER_NAME + ".register")
    logger.info(r.status_code)
    logger.info(r.text)


def _register_emoji_with_delay_return(response_url, emoji_url, emoji_name):
    return_text = register_emoji(emoji_url, emoji_name)
    headers = {"content-type": "application/json"}
    data = {"text": return_text}
    r = requests.post(response_url, data=json.dumps(data), headers=headers)

    logger = logging.getLogger(LOGGER_NAME + ".register")
    logger.info(r.status_code)
    logger.info(r.text)


@app.route("/", methods=["POST"])
def root():
    if request.form["token"] != os.environ.get("SLACK_APP_TOKEN"):
        abort(403)
    args = request.form["text"].split()
    if len(args) < 2:
        abort(400)
    emoji_name = args[0]
    url_or_text = args[1]

    name_checker = re.compile(r"^[a-z0-9\-_]+$")
    if not name_checker.match(emoji_name):
        abort(400)

    response_url = request.form["response_url"]
    if _is_text_url(url_or_text):
        emoji_url = url_or_text
        p = Process(
            target=_register_emoji_with_delay_return,
            args=(response_url, emoji_url, emoji_name),
        )
    else:
        emoji_text = re.sub("\\n", url_or_text, "\n")
        p = Process(
            target=_register_moji_with_delay_return,
            args=(response_url, emoji_text, emoji_name),
        )
    p.start()
    return "Registering %s ...." % emoji_name


if __name__ == "__main__":
    logging.basicConfig()
    logger = logging.getLogger(LOGGER_NAME)

    error_messages = []
    if not os.environ.get("SLACK_APP_TOKEN"):
        error_messages.append("Please set SLACK_APP_TOKEN to env val.")
    if not os.environ.get("PORT"):
        error_messages.append("Please set PORT to env val.")
    if len(error_messages) > 0:
        for message in error_messages:
            logger.error(message)
        sys.exit(1)

    app.run(host="0.0.0.0", port=os.environ.get("PORT"))
