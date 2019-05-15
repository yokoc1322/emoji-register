import emojilib


def main():
    data = emojilib.generate(
        text='絵文\n字',
        # typeface_name='游ゴシック体',
        typeface_file='fonts/NotoSansCJKjp-hinted/NotoSansCJKjp-Bold.otf',
        width=128,
        height=128,
        # color='#FF00FFFF',
        # background_color='#00FF00FF',
        # align='left',  # left, center or right
        # size_fixed=True,
        # disable_stretch=False,
        # format='PNG',  # PING or WEBP
    )

    with open('emoji.png', 'wb') as f:
        f.write(data)


if __name__ == '__main__':
    main()
