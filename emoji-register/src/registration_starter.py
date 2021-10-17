from __future__ import annotations

import json
import pathlib
import re
from multiprocessing import Process

import requests

import slack_emojinator.upload
from emoji_generator import create_random_color, download_image, generate_moji
from logger import get_logger

_IMAGE_DIR = "/tmp"
_RE_URL = re.compile(r"^(http|https)://([-\w]+\.)+[-\w]+(/[-+\w./?%&=]*)?$")

logger = get_logger()


def _register_moji(response_url, text, name):
    logger.info("Recieve: {}: {}".format(text, name))

    color = create_random_color()
    filepath = "/tmp/" + name + ".png"
    generate_moji(text, filepath, color=color)

    response_text = slack_emojinator.upload.upload_main(
        pathlib.Path(filepath).resolve())

    _send_delayed_response(response_url, response_text)
    logger.info('Finish: {}'.format(name))


def _register_emoji(response_url, image_url, name):
    logger.info("Recieve: {}: {}".format(image_url, name))

    try:
        filepath = download_image(image_url, _IMAGE_DIR, name)
        response_text = slack_emojinator.upload.upload_main(filepath.resolve())
    except ValueError:
        response_text = "Not image: " + image_url

    _send_delayed_response(response_url, response_text)
    logger.info('Finish: {}'.format(name))


def _send_delayed_response(url, text):
    logger.info('Send delayed Response: {}'.format(text))
    headers = {"content-type": "application/json"}
    data = {"text": text}
    requests.post(url, data=json.dumps(data), headers=headers)


def _is_text_url(text):
    if _RE_URL.match(text):
        return True
    return False


def start_registration(url_or_text: str, emoji_name: str, response_url: str, is_testing=False):
    if _is_text_url(url_or_text):
        # 画像の場合
        emoji_url = url_or_text
        if is_testing:  # テストのときは登録をマルチプロセスで行わない (すぐに返答を返す必要がないため)
            _register_emoji(response_url, emoji_url, emoji_name)
        else:
            p = Process(
                target=_register_emoji, args=(
                    response_url, emoji_url, emoji_name)
            )
            p.start()

    else:
        # 文字の場合
        emoji_text = re.sub("\\n", url_or_text, "\n")
        if is_testing:  # テストのときは登録をマルチプロセスで行わない (すぐに返答を返す必要がないため)
            _register_moji(response_url, emoji_text, emoji_name)
        else:
            p = Process(
                target=_register_moji, args=(
                    response_url, emoji_text, emoji_name)
            )
            p.start()
