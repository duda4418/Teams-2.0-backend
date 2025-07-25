from datetime import datetime
from uuid import uuid4
from storage.real_db import db


def create_new_message(message_data):
    messages = db.get_messages()

    message_dict = message_data.model_dump()
    message_id = str(uuid4())

    message_dict["id"] = message_id

    time = datetime.now()
    hour = time.hour
    date = time.date()
    if len(str(time.minute)) == 1:
        minute = f"0{time.minute}"
    else:
        minute = time.minute
    message_dict["time"] = f"{date}    {hour}:{minute}"

    messages[message_id] = message_dict

    db.create_message(
        message_id=message_dict["id"],
        discussion_id=message_dict["discussion_id"],
        user_id=message_dict["user_id"],
        value=message_dict["value"],
        time=message_dict["time"])

    return message_dict

def get_messages_by_discussion_id(discussion_id):

    messages = db.get_messages()
    users_dict = db.get_users()

    message_list = []
    for key in messages:
        message = messages[key]
        if message.get("discussion_id") == discussion_id:
            message["name"] = users_dict.get(message.get("user_id"), {}).get("name")
            message_list.append(message)
    return message_list


