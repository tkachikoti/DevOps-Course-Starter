import json

from todo_app.app import create_app

def test_index_get_route(load_fake_environment_variables):
    # Create the app and push an application context
    test_app = create_app()
    with test_app.test_client() as client:
        collection_name = "TASKS_COLLECTION"
        # Load mock data into the temporary collection
        with open('todo_app/tests/tasks_collection_mock_data.json', 'r') as file:
            mock_data = json.load(file)

        # Access the app context to use mongo_db_manager
        with test_app.app_context():
            for item in mock_data:
                test_app.mongo_db_manager.insert_document(
                    collection_name, item
                )

        response = client.get('/')
        assert response.status_code == 200
        assert 'Write MongoDB module' in response.data.decode()


def test_add_todo_item_get_route(client):
    response = client.get('/add-todo-item')
    assert response.status_code == 200
    assert 'ADD TODO ITEM' in response.data.decode()
