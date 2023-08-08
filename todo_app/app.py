from flask import Flask, render_template, redirect, url_for, request

from todo_app.data.item import Item
from todo_app.data.trello_items import (
    get_items, get_item, add_item, delete_item, save_item
)
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/', methods=['GET'])
def index():
    return render_template(
        'index.html',
        list_of_items=get_items()
    )


@app.route('/add_todo_item', methods=['POST'])
def add_todo_item():
    item = Item(request.form['title'])
    add_item(item)

    return redirect(url_for('index'))


@app.route('/delete_item/<id>', methods=['GET'])
def delete_todo_item(id):
    delete_item(id)
    return redirect(url_for('index'))


@app.route('/complete_item/<id>', methods=['GET'])
def mark_todo_item_complete(id):
    item = get_item(id)
    if item:
        item.mark_as_complete()
        save_item(item)
    return redirect(url_for('index'))


@app.route('/not_started_item/<id>', methods=['GET'])
def mark_todo_item_not_started(id):
    item = get_item(id)
    if item:
        item.mark_as_not_started()
        save_item(item)
    return redirect(url_for('index'))
