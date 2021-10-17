import os
import re
from pathlib import Path

import pytest
from emoji_generator import create_random_color, download_image, generate_moji

IMAGE_FILE_NAME = "image"
IMAGE_FILE_DIR = "/tmp"
IMAGE_FILE_PATH = "/tmp/image.png"


@pytest.fixture
def delete_image_file():
    if Path(IMAGE_FILE_PATH).exists():
        os.remove(IMAGE_FILE_PATH)
    yield
    if Path(IMAGE_FILE_PATH).exists():
        os.remove(IMAGE_FILE_PATH)


def test_create_random_color():
    color_code = create_random_color()
    assert re.match(r"[0-9A-F]{6}FF", color_code) is not None


def test_generate_moji(delete_image_file):
    text = "麗"
    generate_moji(text, IMAGE_FILE_PATH)
    assert Path(IMAGE_FILE_PATH).exists()


def test_download_image(delete_image_file):
    url = "https://emojis.slackmojis.com/emojis/images/1450319441/51/facepalm.png?1450319441"
    download_image(url, IMAGE_FILE_DIR, IMAGE_FILE_NAME)
    assert Path(IMAGE_FILE_PATH).exists()
