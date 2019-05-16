import os
import re
from flask import Flask, request, abort
from emoji import register_emoji
app = Flask(__name__)


@app.route('/', methods=['POST'])
def route():
    if request.form['token'] != os.environ.get('SLACK_APP_TOKEN'):
        abort(403)
    args = request.form['text'].split()
    if len(args) < 2:
        abort(400)
    emoji_text = re.sub('\\n', args[0], '\n')
    emoji_name = args[1]
    name_checker = re.compile(r"^[a-z0-9\-_]+$")

    if not name_checker.match(emoji_name):
        abort(400)

    register_emoji(emoji_text, emoji_name)

    return "Hello"


if __name__ == '__main__':
    if not os.environ.get('SLACK_APP_TOKEN'):
        print("Please set SLACK_APP_TOKEN to env val ")
    else:
        app.run(host='0.0.0.0', port=80)
