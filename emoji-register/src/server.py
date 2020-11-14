import json
import logging
import os
import pathlib
import re
import sys
from multiprocessing import Process

import requests
from flask import Flask, abort, request

import emoji
import slack_emojinator.upload

LOGGER_NAME = "emoji_register.server"
IMAGE_DIR = "/tmp"
RE_URL = re.compile(r"^(http|https)://([-\w]+\.)+[-\w]+(/[-+\w./?%&=]*)?$")

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(LOGGER_NAME)


def _is_text_url(text):
    if RE_URL.match(text):
        return True
    return False


def _register_moji(response_url, text, name):
    logger.info("Recieve: {}: {}".format(text, name))

    color = emoji.create_random_color()
    filepath = "/tmp/" + name + ".png"
    emoji.generate_moji(text, filepath, color=color)
    response_text = slack_emojinator.upload.upload_main(
        pathlib.Path(filepath).resolve())
    _send_delayed_response(response_url, response_text)
    logger.info('Finish: {}'.format(name))


def _register_emoji(response_url, image_url, name):
    logger.info("Recieve: {}: {}".format(image_url, name))

    try:
        filepath = emoji.download_image(image_url, IMAGE_DIR, name)
        response_text = slack_emojinator.upload.upload_main(filepath.resolve())
    except ValueError:
        response_text = "Not image: " + image_url
    _send_delayed_response(response_url, response_text)
    logger.info('Finish: {}'.format(name))


def _send_delayed_response(url, text):
    logger.info('Send delayed Response: {}'.format(text))
    headers = {"content-type": "application/json"}
    data = {"text": text}
    r = requests.post(url, data=json.dumps(data), headers=headers)


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
