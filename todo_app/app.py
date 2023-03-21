from flask import Flask, render_template

from todo_app.data.session_items import get_items

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    return render_template(
        'index.html',
        list_of_items=get_items())
