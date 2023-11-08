import json
from uuid import uuid4
from storage.fake_db import fake_db


def create_new_message(message_data):
    messages = fake_db.get("messages", {})

    message_dict = message_data.model_dump()
    message_id = str(uuid4())

    message_dict["id"] = message_id

    messages[message_id] = message_dict

    with open("storage/messages.json", "w") as file:
        json.dump(messages, file, default=str)

def get_messages_by_discussion_id(discussion_id):

    messages = list(fake_db.get("messages", {}).values())
    users_dict = fake_db.get("users", {})

    message_list = []
    for message in messages:
        if message.get("discussion_id") == discussion_id:
            message["name"] = users_dict.get(message.get("user_id"), {}).get("name")
            message_list.append(message)
    return message_list


