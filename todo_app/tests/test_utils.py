import json
import os

from dotenv import find_dotenv


class StubResponse():
    def __init__(self, fake_response_data, status_code=200):
        self.fake_response_data = fake_response_data
        self._status_code = status_code

    def json(self):
        return self.fake_response_data

    @property
    def status_code(self):
        return self._status_code


def stub(url, params={}):
    test_board_id = os.environ.get('TRELLO_BOARD_ID')
    if url == f'https://api.trello.com/1/boards/{test_board_id}/cards':
        return mock_get_cards_endpoint()
    elif url == 'https://api.trello.com/1/boards':
        return StubResponse([{'id': test_board_id}])
    raise Exception(f'Integration test did not expect URL "{url}"')


def mock_get_cards_endpoint():
    mock_data_file_path = find_dotenv('trello_cards_mock_data.json')
    with open(mock_data_file_path, 'r') as file:
        fake_response_data = json.load(file)

        return StubResponse(fake_response_data)
