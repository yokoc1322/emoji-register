from slack_emojinator.upload import upload_main
import emojilib
import pathlib
import random

_DEFAULT_FONT_FILE = 'fonts/NotoSansCJKjp-hinted/NotoSansCJKjp-Bold.otf'


def _create_random_color():
    COLOR_TABLE = ['FF', '88', '00']
    TABLE_LENGTH = len(COLOR_TABLE)
    RAND_MAX = 100

    # 一定上の濃さになるまで回す
    sum = 0
    while sum < 1:
        red = random.randrange(0, RAND_MAX) % TABLE_LENGTH
        blue = random.randrange(0, RAND_MAX) % TABLE_LENGTH
        green = random.randrange(0, RAND_MAX) % TABLE_LENGTH
        sum = red + blue + green
    return COLOR_TABLE[red] + COLOR_TABLE[blue] + COLOR_TABLE[green] + 'FF'


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