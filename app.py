# pylint: disable=protected-access missing-function-docstring missing-module-docstring missing-class-docstring
from pathlib import Path

from flask import Flask, render_template
from flask_socketio import SocketIO


from ws import main as ws_main

ROOT = Path(__file__).parent / 'web'

app = Flask(
    __name__,
    static_folder=f'{ROOT}/static',
    static_url_path='/static',
    template_folder=f'{ROOT}/templates'
)
socketio = SocketIO(app)
ws_main(socketio)


@app.route('/')
def index():
    with open(f"{ROOT}/index.html", encoding="utf8") as f:
        return f.read()

if __name__ == '__main__':
    socketio.run(app, port=42501, host="0.0.0.0",
                 debug=True, use_reloader=False, log_output=True)
