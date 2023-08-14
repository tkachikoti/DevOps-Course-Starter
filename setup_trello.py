"""
This module provides a script to update the Trello-related values in a
specified .env file using the ID of a given Trello board.
It requires the Trello API key, API token, and Board ID, and updates the IDs
of the "To Do", "Doing", and "Done" lists on the specified board.

Usage:
    poetry run python setup_trello.py

Dependencies:
    - os
    - requests
    - dotenv
"""


import os
import requests

from dotenv import load_dotenv, find_dotenv

load_dotenv()

TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_API_TOKEN = os.getenv("TRELLO_API_TOKEN")
TRELLO_BOARD_ID = os.getenv("TRELLO_BOARD_ID")


def update_env_file():
    # Get the lists on the board
    lists_url = (
        f"https://api.trello.com/1/boards/{TRELLO_BOARD_ID}/lists"
        f"?key={TRELLO_API_KEY}&token={TRELLO_API_TOKEN}"
    )
    response = requests.get(lists_url)
    lists = response.json()

    # Function to check list name ignoring case and whitespace
    def check_list_name(list_, name):
        return list_['name'].strip().lower() == name.lower()

    # Assuming the lists have specific names for "To Do", "Doing" and "Done"
    trello_todo_list_id = next(
        list_['id'] for list_ in lists if check_list_name(list_, 'To Do')
    )
    trello_doing_list_id = next(
        list_['id'] for list_ in lists if check_list_name(list_, 'Doing')
    )
    trello_done_list_id = next(
        list_['id'] for list_ in lists if check_list_name(list_, 'Done')
    )

    # Path to the .env file
    env_file_path = find_dotenv('.env')

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
