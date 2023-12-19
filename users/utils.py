from uuid import uuid4
from storage.real_db import db


def get_user_data(user_data):
    users = db.get_users()
    for id in users:
        user = users[id]
        name = user.get("name")
        password = user.get("password")
        if name == user_data.name and password == user_data.password:
            return users[id]
    return None

def create_user(data):
    users = db.get_users()

    user_id = str(uuid4())
    user_data = data.model_dump()
    user_data["id"] = user_id
    users[user_id] = user_data

    db.create_user(name=user_data.get("name"), password=user_data.get("password"), user_id=user_id)

    return user_data