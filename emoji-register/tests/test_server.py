import sys
from pathlib import Path
from unittest.mock import patch
import pytest
sys.path.append(str(Path(__file__).parents[1].resolve() / "src"))
import server

TOKEN = "DUMMY_TOKEN"


@pytest.fixture
def client():
    server.app.config["TESTING"] = True
    server.app.config["SLACK_APP_TOKEN"] = TOKEN
    client = server.app.test_client()
    yield client


CORRECT_TEXT_MOJI = "name te\\nxt"
CORRECT_TEXT_EMOJI = "name https://www.image.dummy.co.jp/image.png"
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
@patch("server._register_moji")
@patch("server._register_emoji")
def test_status_code(r_emoji, r_moji, client, data, expected_code):
    data = {
        "token": data["token"],
        "text": data["text"],
        "response_url": data["response_url"],
    }

    r = client.post("/", data=data)
    if expected_code == 200:
        assert r_moji.called
    assert r.status_code == expected_code


@patch("emoji.generate_moji")
@patch("slack_emojinator.upload.upload_main", return_value="debug")
@patch("requests.post")
def test_to_use_register_moji(r_requests, r_upload, r_moji, client):
    data = {
        "token": TOKEN,
        "text": CORRECT_TEXT_MOJI,
        "response_url": CORRECT_RESPONSE_URL,
    }
    client.post("/", data=data)
    assert r_moji.call_count == 1
    assert r_upload.call_count == 1
    assert r_requests.call_count == 1


@patch("emoji.download_image")
@patch("slack_emojinator.upload.upload_main", return_value="debug")
@patch("requests.post")
def test_to_use_register_emoji(r_requests, r_upload, r_emoji, client):
    data = {
        "token": TOKEN,
        "text": CORRECT_TEXT_EMOJI,
        "response_url": CORRECT_RESPONSE_URL,
    }
    client.post("/", data=data)
    assert r_emoji.call_count == 1
    assert r_upload.call_count == 1
    assert r_requests.call_count == 1


@pytest.mark.parametrize(
    "url, result", [
        ("https://www.google.co.jp/logos/doodles/2019/summer-2019-northern-hemisphere-6566840133222400-l.png", True),
        ("ftp://hello-world.co.jp", False),
        ("hello", False),
        ("https://www.google.com/search?ei=nKILXeWtIoyA8QXZ1LPYCQ&q=hello+world&oq=hello+world", True),
        ("", False)
    ])
def test_is_text_url(url, result):
    assert server._is_text_url(url) is result
