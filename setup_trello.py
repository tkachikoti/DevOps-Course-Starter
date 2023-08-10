"""
This script updates the Trello-related values in a specified .env file using
the ID of a given Trello board.

The script requires the following information:
- Trello API Key
- Trello API Token
- Trello Board ID (provided as a command-line argument)

It will fetch the board ID and the IDs of the "Not Started" and "Complete"
lists from the specified board and update the corresponding values in
the .env file.

Usage:
    python script.py <Trello Board ID>
"""

import os
import requests

from dotenv import load_dotenv

load_dotenv()

TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_API_TOKEN = os.getenv("TRELLO_API_TOKEN")
TRELLO_BOARD_ID = os.getenv("TRELLO_BOARD_ID")


def update_env_file():
    # Get the lists on the board
    lists_url = f"https://api.trello.com/1/boards/{TRELLO_BOARD_ID}/lists?key={TRELLO_API_KEY}&token={TRELLO_API_TOKEN}"
    response = requests.get(lists_url)
    lists = response.json()

    # Assuming the lists have specific names for "To Do", "Doing" and "Done"
    trello_todo_list_id = next(list_['id'] for list_ in lists if list_['name'] == 'To Do')
    trello_doing_list_id = next(list_['id'] for list_ in lists if list_['name'] == 'Doing')
    trello_done_list_id = next(list_['id'] for list_ in lists if list_['name'] == 'Done')

    # Path to the .env file
    env_file_path = '.env'

    # Read the existing .env file content
    with open(env_file_path, 'r') as file:
        env_content = file.readlines()

    # Modify the content with the new values
    new_content = []
    for line in env_content:
        if 'TRELLO_TODO_LIST_ID' in line:
            line = f"TRELLO_TODO_LIST_ID={trello_todo_list_id}\n"
        elif 'TRELLO_DOING_LIST_ID' in line:
            line = f"TRELLO_DOING_LIST_ID={trello_doing_list_id}\n"
        elif 'TRELLO_DONE_LIST_ID' in line:
            line = f"TRELLO_DONE_LIST_ID={trello_done_list_id}\n"
        new_content.append(line)

    # Write the modified content back to the .env file
    with open(env_file_path, 'w') as file:
        file.writelines(new_content)

    print("Updated .env file with Trello details.")


if __name__ == "__main__":

    update_env_file()
