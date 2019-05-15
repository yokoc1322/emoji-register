from flask import Flask, request
from emoji import register_emoji
app = Flask(__name__)


@app.route('/', methods=['POST'])
def route():
    register_emoji('絵\n文', 'e')
    print(request.args)
    return "Hello"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
