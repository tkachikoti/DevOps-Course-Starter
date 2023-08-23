"""
This module provides a script to update the Trello-related values in a
specified .env file.
It requires the Trello API key and an API token, and updates the IDs of
the Trello Board, "To Do", "Doing", and "Done" lists on the specified board.

Usage:
    poetry run python setup_trello.py

Dependencies:
    - time
    - dotenv
"""

from time import sleep

from dotenv import load_dotenv, find_dotenv

from todo_app.data.trello_items import create_board, create_list_on_board

load_dotenv()

RATE_LIMIT_DELAY_IN_SECONDS = 0.2


def setup_trello():
    # Create a new board
    trello_board_name = "APP STORAGE: To-Do List"
    new_trello_board = create_board(trello_board_name)

    # Create the lists on the board
    trello_lists = {
        "Done": "done-list-id",
        "Doing": "doing-list-id",
        "To Do": "todo-list-id"
    }

    for name in trello_lists.keys():
        new_trello_list = create_list_on_board(name, new_trello_board["id"])
        trello_lists[name] = new_trello_list["id"]
        sleep(RATE_LIMIT_DELAY_IN_SECONDS)
        print(f"'{name}' List created\n")

    # Path to the .env file
    env_file_path = find_dotenv('.env')

    # Read the existing .env file content
    with open(env_file_path, 'r') as file:
        env_content = file.readlines()

    # Modify the content with the new values
    new_content = []
    for line in env_content:
        if 'TRELLO_TODO_LIST_ID' in line:
            line = f"TRELLO_TODO_LIST_ID={trello_lists['To Do']}\n"
        elif 'TRELLO_DOING_LIST_ID' in line:
            line = f"TRELLO_DOING_LIST_ID={trello_lists['Doing']}\n"
        elif 'TRELLO_DONE_LIST_ID' in line:
            line = f"TRELLO_DONE_LIST_ID={trello_lists['Done']}\n"
        elif 'TRELLO_BOARD_ID' in line:
            line = f"TRELLO_BOARD_ID={new_trello_board['id']}\n"
        new_content.append(line)

    # Write the modified content back to the .env file
    with open(env_file_path, 'w') as file:
        file.writelines(new_content)

    print("Updated .env file with Trello details.")


if __name__ == "__main__":
    setup_trello()
