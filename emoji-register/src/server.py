import os
import re
import sys
import json
import logging
import pathlib
from multiprocessing import Process

import requests
from flask import Flask, request, abort

import emoji
import slack_emojinator.upload

LOGGER_NAME = "emoji_register"
IMAGE_DIR = "/tmp"
RE_URL = re.compile(r"^(http|https)://([-\w]+\.)+[-\w]+(/[-+\w./?%&=]*)?$")

app = Flask(__name__)


def _is_text_url(text):
    if RE_URL.match(text):
        return True
    return False


def _register_moji(response_url, text, name):
    color = emoji.create_random_color()
    filepath = "/tmp/" + name + ".png"
    emoji.generate_moji(text, filepath, color=color)
    response_text = slack_emojinator.upload.upload_main(
        pathlib.Path(filepath).resolve())
    _send_delayed_response(response_url, response_text)


def _register_emoji(response_url, image_url, name):
    try:
        filepath = emoji.download_image(image_url, IMAGE_DIR, name)
        response_text = slack_emojinator.upload.upload_main(filepath.resolve())
    except ValueError:
        response_text = "Not image: " + image_url
    _send_delayed_response(response_url, response_text)


def _send_delayed_response(url, text):
    headers = {"content-type": "application/json"}
    data = {"text": text}
    r = requests.post(url, data=json.dumps(data), headers=headers)

    logger = logging.getLogger(LOGGER_NAME + ".register")
    logger.info(r.status_code)
    logger.info(r.text)


@app.route("/", methods=["POST"])
def root():
    if request.form["token"] != app.config["SLACK_APP_TOKEN"]:
        abort(403)
    args = request.form["text"].split()
    if len(args) < 2:
        abort(400)
    url_or_text = args[0]
    emoji_name = args[1]

    name_checker = re.compile(r"^[a-z0-9\-_]+$")
    if not name_checker.match(emoji_name):
        abort(400)

    response_url = request.form["response_url"]
    if _is_text_url(url_or_text):
        emoji_url = url_or_text
        if app.config["TESTING"]:
            _register_emoji(response_url, emoji_url, emoji_name)
        else:
            p = Process(
                target=_register_emoji, args=(
                    response_url, emoji_url, emoji_name)
            )
            p.start()

    else:
        emoji_text = re.sub("\\n", url_or_text, "\n")
        if app.config["TESTING"]:
            _register_moji(response_url, emoji_text, emoji_name)
        else:
            p = Process(
                target=_register_moji, args=(
                    response_url, emoji_text, emoji_name)
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

    app.config["SLACK_APP_TOKEN"] = os.environ.get("SLACK_APP_TOKEN")
    app.run(host="0.0.0.0", port=os.environ.get("PORT"))
