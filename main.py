import emojilib

_DEFAULT_FONT_FILE = 'fonts/NotoSansCJKjp-hinted/NotoSansCJKjp-Bold.otf'


def generate(
    text='',
    typeface_file=_DEFAULT_FONT_FILE,
    width=128,
    height=128,
    align='center',
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
        **generate_options,
        # format='PNG',  # PING or WEBP
    )

    with open('emoji.png', 'wb') as f:
        f.write(data)


if __name__ == '__main__':
    generate('絵文\n字')
