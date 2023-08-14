from flask import Flask, render_template, redirect, url_for, request

from todo_app.data.item import Item
from todo_app.data.view_model import ViewModel
from todo_app.data.trello_items import (
    get_items, get_item, add_item, delete_item, save_item
)
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/', methods=['GET'])
def index():

    item_view_model = ViewModel(get_items())
    return render_template(
        'index.html',
        view_model=item_view_model
    )


@app.route('/add-todo-item', methods=['GET', 'POST'])
def add_todo_item():
    if request.method == 'GET':
        return render_template('add-todo-item.html')
    else:
        item = Item(title=request.form.get('title', None),
                    description=request.form.get('description', None),
                    due_date=request.form.get('due_date', None))
        add_item(item)

        return redirect(url_for('index'))


@app.route('/delete-item/<id>', methods=['GET'])
def delete_todo_item(id):
    delete_item(id)
    return redirect(url_for('index'))


@app.route('/not-started-item/<id>', methods=['GET'])
def mark_todo_item_not_started(id):
    item = get_item(id)
    if item:
        item.mark_as_to_do()
        save_item(item)
    return redirect(url_for('index'))


@app.route('/in-progress-item/<id>', methods=['GET'])
def mark_todo_item_in_progress(id):
    item = get_item(id)
    if item:
        item.mark_as_doing()
        save_item(item)
    return redirect(url_for('index'))


@app.route('/complete-item/<id>', methods=['GET'])
def mark_todo_item_complete(id):
    item = get_item(id)
    if item:
        item.mark_as_done()
        save_item(item)
    return redirect(url_for('index'))
