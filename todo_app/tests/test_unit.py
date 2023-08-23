def test_view_model_todo_items(example_view_model_items):
    assert len(example_view_model_items.todo_items) > 0
    assert all(
        item.status == "To Do" for item in example_view_model_items.todo_items
    )


def test_view_model_doing_items(example_view_model_items):
    assert len(example_view_model_items.doing_items) > 0
    assert all(
        item.status == "Doing" for item in example_view_model_items.doing_items
    )


def test_view_model_done_items(example_view_model_items):
    assert len(example_view_model_items.done_items) > 0
    assert all(
        item.status == "Done" for item in example_view_model_items.done_items
    )
