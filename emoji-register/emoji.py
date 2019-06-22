from slack_emojinator.upload import upload_main
import emojilib
import pathlib
import random
import requests
from functools import reduce

_DEFAULT_FONT_FILE = "fonts/NotoSansCJKjp-hinted/NotoSansCJKjp-Bold.otf"


def _create_random_color():
    COLOR_MIN = 0
    COLOR_MAX = 255
    AVG_MAX = 200

    # 一定上の濃さになるまで回す
    avg = COLOR_MAX
    while avg > AVG_MAX:
        red = random.randint(COLOR_MIN, COLOR_MAX)
        blue = random.randint(COLOR_MIN, COLOR_MAX)
        green = random.randint(COLOR_MIN, COLOR_MAX)
        avg = (red + blue + green) / 3
    return "%02X%02X%02XFF" % (red, blue, green)


def _is_every_line_1_char(text):
    is_line_1_char = map(lambda x: len(x) == 1, text.split("\n"))
    return reduce(lambda x, acc: x and acc, is_line_1_char, True)


def _download_image(url, dir, name):
    response = requests.get(url)
    content_type = response.headers["Content-Type"].split("/")

    if content_type[0] != "image":
        # TODO: 例外の型含め、エラー時の挙動を考える
        raise ValueError("It's not image")
    print(content_type)

    filename = "%s.%s" % (name, content_type[1])
    filepath = pathlib.Path(dir).joinpath(filename)
    with open(filepath, "wb") as image_file:
        image_file.write(response.content)

    return filepath


def generate(
    text,
    filename,
    typeface_file=_DEFAULT_FONT_FILE,
    width=128,
    height=128,
    default_align="left",
    color=None,
    background_color=None,
    size_fixed=None,
    disable_stretch=None,
):
    generate_options = {}
    if color:
        generate_options["color"] = color
    if background_color:
        generate_options["background_color"] = background_color
    if size_fixed:
        generate_options["size_fixed"] = size_fixed
    if disable_stretch:
        generate_options["disable_stretch"] = disable_stretch
    align = "center" if _is_every_line_1_char(text) else default_align

    data = emojilib.generate(
        text=text,
        # typeface_name='游ゴシック体',
        typeface_file=typeface_file,
        width=width,
        height=height,
        align=align,
        **generate_options,
        # format='PNG',  # PING or WEBP
    )

    with open(filename, "wb") as f:
        f.write(data)


def register_moji(text, name):
    color = _create_random_color()
    filepath = "/tmp/" + name + ".png"
    generate(text, filepath, color=color)
    return upload_main(pathlib.Path(filepath).resolve())


def register_emoji(url, name):
    dir = "/tmp"
    try:
        filepath = _download_image(url, dir, name)
    except ValueError:
        return "It's not image"
    return upload_main(filepath.resolve())
