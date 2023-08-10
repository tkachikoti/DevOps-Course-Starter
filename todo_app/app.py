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
    sort_options = {
        'sort_by': request.args.get('sort_by', 'status'),
        'order_by_descending': request.args.get('order_by_descending', '0')
    }

    sort_by = sort_options['sort_by']
    order_by_descending = bool(int(sort_options['order_by_descending']))
    # items = ViewModel(items)
    return render_template(
        'index.html',
        sort_options=sort_options,
        list_of_items=sorted(
            get_items(),
            key=lambda item: getattr(item, f'get_{sort_by}')(),
            reverse=order_by_descending)
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


@app.route('/complete-item/<id>', methods=['GET'])
def mark_todo_item_complete(id):
    item = get_item(id)
    if item:
        item.mark_as_complete()
        save_item(item)
    return redirect(url_for('index'))


@app.route('/not-started-item/<id>', methods=['GET'])
def mark_todo_item_not_started(id):
    item = get_item(id)
    if item:
        item.mark_as_not_started()
        save_item(item)
    return redirect(url_for('index'))
