import os
import sys
import re
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).parents[1] / "src"))

import emoji

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
    color_code = emoji.create_random_color()
    assert re.match(r"[0-9A-F]{6}FF", color_code) is not None


def test_generate_moji(delete_image_file):
    text = "麗"
    emoji.generate_moji(text, IMAGE_FILE_PATH)
    assert Path(IMAGE_FILE_PATH).exists()


def test_download_image(delete_image_file):
    url = "https://emojis.slackmojis.com/emojis/images/1450319441/51/facepalm.png?1450319441"
    emoji.download_image(url, IMAGE_FILE_DIR, IMAGE_FILE_NAME)
    assert Path(IMAGE_FILE_PATH).exists()
