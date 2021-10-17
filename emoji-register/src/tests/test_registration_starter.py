from __future__ import annotations
import pytest

from registration_starter import _is_text_url


@pytest.mark.parametrize(
    "url, result", [
        ("https://www.google.co.jp/logos/doodles/2019/summer-2019-northern-hemisphere-6566840133222400-l.png", True),
        ("ftp://hello-world.co.jp", False),
        ("hello", False),
        ("https://www.google.com/search?ei=nKILXeWtIoyA8QXZ1LPYCQ&q=hello+world&oq=hello+world", True),
        ("", False)
    ])
def test_is_text_url(url, result):
    assert _is_text_url(url) is result


# @patch("emoji.generate_moji")
# @patch("slack_emojinator.upload.upload_main", return_value="debug")
# @patch("requests.post")
# def test_to_use_register_moji(r_requests, r_upload, r_moji, client):
#     data = {
#         "token": TOKEN,
#         "text": CORRECT_TEXT_MOJI,
#         "response_url": CORRECT_RESPONSE_URL,
#     }
#     client.post("/", data=data)
#     assert r_moji.call_count == 1
#     assert r_upload.call_count == 1
#     assert r_requests.call_count == 1


# @patch("emoji.download_image")
# @patch("slack_emojinator.upload.upload_main", return_value="debug")
# @patch("requests.post")
# def test_to_use_register_emoji(r_requests, r_upload, r_emoji, client):
#     data = {
#         "token": TOKEN,
#         "text": CORRECT_TEXT_EMOJI,
#         "response_url": CORRECT_RESPONSE_URL,
#     }
#     client.post("/", data=data)
#     assert r_emoji.call_count == 1
#     assert r_upload.call_count == 1
#     assert r_requests.call_count == 1
