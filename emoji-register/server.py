import os
import re
import sys
from flask import Flask, request, abort
from emoji import register_emoji

app = Flask(__name__)


@app.route("/", methods=["POST"])
def route():
    if request.form["token"] != os.environ.get("SLACK_APP_TOKEN"):
        abort(403)
    args = request.form["text"].split()
    if len(args) < 2:
        abort(400)
    emoji_text = re.sub("\\n", args[0], "\n")
    emoji_name = args[1]
    name_checker = re.compile(r"^[a-z0-9\-_]+$")

    if not name_checker.match(emoji_name):
        abort(400)

    return register_emoji(emoji_text, emoji_name)


if __name__ == "__main__":
    error_message = ""
    if not os.environ.get("SLACK_APP_TOKEN"):
        error_message += "Please set SLACK_APP_TOKEN to env val.\n"
    if not os.environ.get("PORT"):
        error_message += "Please set PORT to env val.\n"
    if len(error_message) > 0:
        print(error_message)
        sys.exit(1)

    app.run(host="0.0.0.0", port=os.environ.get("PORT"))
