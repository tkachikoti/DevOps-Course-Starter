from flask import Flask, render_template, redirect, url_for, request

from todo_app.data.session_items import get_items, add_item

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/', methods=['GET'])
def index():
    return render_template(
        'index.html',
        list_of_items=get_items())

@app.route('/add_todo_item', methods=['POST'])
def add_todo_item():

    add_item(request.form['title'])

    return redirect(url_for('index'))
