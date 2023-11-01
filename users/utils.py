import json

from storage.fake_db import fake_db
from uuid import uuid4

def get_user_data(user_data):
    users = fake_db.get("users", {}).values()
    for user in users:
        name = user.get("name")
        password = user.get("password")
        if name == user_data.name and password == user_data.password:
            return user
    return None

def create_user(data):
    users = fake_db.get("users", {})

    user_id = str(uuid4())
    user_data = data.model_dump()
    user_data["id"] = user_id
    users[user_id] = user_data

    with open("storage/users.json", "w") as file:
        json.dump(users, file, default=str)

    return user_data