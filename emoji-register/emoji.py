from slack_emojinator.upload import upload_main
import emojilib
import pathlib
import random

_DEFAULT_FONT_FILE = 'fonts/NotoSansCJKjp-hinted/NotoSansCJKjp-Bold.otf'


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
    return '%02X%02X%02XFF' % (red, blue, green)


def generate(
    text,
    filename,
    typeface_file=_DEFAULT_FONT_FILE,
    width=128,
    height=128,
    align='left',
    color=None,
    background_color=None,
    size_fixed=None,
    disable_stretch=None
):
    generate_options = {}
    if color:
        generate_options['color'] = color
    if background_color:
        generate_options['background_color'] = background_color
    if size_fixed:
        generate_options['size_fixed'] = size_fixed
    if disable_stretch:
        generate_options['disable_stretch'] = disable_stretch

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

    with open(filename, 'wb') as f:
        f.write(data)


def register_emoji(text, name):
    color = _create_random_color()
    filename = '/tmp/' + name + '.png'
    generate(text, filename, color=color)
    return upload_main(pathlib.Path(filename).resolve())
