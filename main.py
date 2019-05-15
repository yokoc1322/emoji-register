from slack_emojinator.upload import upload_main
import emojilib
import pathlib
import random

_DEFAULT_FONT_FILE = 'fonts/NotoSansCJKjp-hinted/NotoSansCJKjp-Bold.otf'


def _create_random_color():
    COLOR_TABLE = ['00', '88', 'FF']
    TABLE_LENGTH = len(COLOR_TABLE)
    RAND_MAX = 100

    # 一定上の濃さになるまで回す
    sum = 0
    while sum < 2:
        red = random.randrange(0, RAND_MAX) % TABLE_LENGTH
        blue = random.randrange(0, RAND_MAX) % TABLE_LENGTH
        green = random.randrange(0, RAND_MAX) % TABLE_LENGTH
        sum = red + blue + green
    return COLOR_TABLE[red] + COLOR_TABLE[blue] + COLOR_TABLE[green] + 'FF'


def generate(
    text='',
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

    with open('emoji.png', 'wb') as f:
        f.write(data)


if __name__ == '__main__':
    color = _create_random_color()
    generate('絵文\n字', color=color)
    # upload_main(pathlib.Path('./emoji.png').resolve())
