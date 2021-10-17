from __future__ import annotations
from unittest.mock import patch, MagicMock

import pytest
import server

TOKEN = "DUMMY_TOKEN"


@pytest.fixture
def client():
    server.app.config["TESTING"] = True
    server.app.config["SLACK_APP_TOKEN"] = TOKEN
    client = server.app.test_client()
    yield client


CORRECT_TEXT_MOJI = "te\\nxt name"
CORRECT_TEXT_EMOJI = "https://www.image.dummy.co.jp/image.png name"
CORRECT_RESPONSE_URL = "https://httpbin.org/post"


@pytest.mark.parametrize(
    "data, expected_code",
    [
        ({"token": TOKEN,
          "text": CORRECT_TEXT_MOJI,
          "response_url": CORRECT_RESPONSE_URL},
         200),
        ({"token": "INVALID_TOKEN",
          "text": CORRECT_TEXT_MOJI,
          "response_url": CORRECT_RESPONSE_URL},
         403),
        ({"token": TOKEN,
          "text": "",
          "response_url": CORRECT_RESPONSE_URL},
         400),
        ({"token": TOKEN,
          "text": "first",
          "response_url": CORRECT_RESPONSE_URL},
         400)
    ],
)
@patch("server.start_registration")
def test_status_code(mock_start_registration: MagicMock, client, data, expected_code):
    data = {
        "token": data["token"],
        "text": data["text"],
        "response_url": data["response_url"],
    }

    r = client.post("/", data=data)
    assert r.status_code == expected_code
    if expected_code == 200:
        mock_start_registration.assert_called()
