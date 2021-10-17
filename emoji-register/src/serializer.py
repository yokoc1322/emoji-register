from __future__ import annotations

import re
from typing import Any


class UnValidError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__()


def is_valid_token(expected_token: str, actual_token: str):
    if expected_token != actual_token:
        return False
    return True


def validate_registration_params(params: dict[str, Any]) -> tuple[str, str, str]:
    """
    Returns:
        str: 登録する絵文字の文字、もしくは画像のURL
        str: 絵文字の名前
        str: 登録が完了した際に応答を投げるURL
    """

    args = params["text"].split()
    if len(args) < 2:
        raise UnValidError(message="too few args")
    url_or_text = args[0]
    emoji_name = args[1]

    name_checker = re.compile(r"^[a-z0-9\-_]+$")
    if not name_checker.match(emoji_name):
        raise UnValidError(message="unvalid name")

    response_url = params["response_url"]

    return url_or_text, emoji_name, response_url
