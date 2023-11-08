import json
from uuid import uuid4

from storage.fake_db import fake_db


def get_contact_discussions(discussion_data):
    discussions = fake_db.get("discussions",{}).values()
    for discussion in discussions:
        contact_id = discussion.get("contacts")
        if contact_id in discussion_data:
                return discussion
    return None

def create_new_discussion(data):
    discussions = fake_db.get("discussions", {})

    discussion_id = str(uuid4())
    discussion_data = data.model_dump()
    discussion_data["id"] = discussion_id
    discussions[discussion_id] = discussion_data

    with open("storage/discussions.json", "w") as file:
        json.dump(discussions, file, default=str)

    return discussion_data

def get_discussions(user_id):
    users = fake_db.get("users", {})
    discussions = fake_db.get("discussions", {}).values()

    discussions_list = []

    for discussion in discussions:
        contacts = discussion.get("contacts", [])

        one_to_one_discussion = contacts[0] != contacts[1]
        yourself_discussion = contacts[0] == contacts[1]

        if user_id in contacts:
            if one_to_one_discussion:
                for contact in contacts:
                    if user_id != contact:
                        discussion["name"] = users.get(contact)["name"]
            elif yourself_discussion:
                contact = contacts[0]
                if user_id == contact:
                    discussion["name"] = users.get(contact)["name"]
            discussions_list.append(discussion)
    return discussions_list

def remove_duplicate_contacts(contacts):
    return [contact for index, contact in enumerate(contacts) if contact not in contacts[:index]]

    """discussion_list = []
    for discussion in discussions:
        discussions_id = discussion.get("contacts", [])
        if user_id in discussions_id:
            discussion_list.append(discussion)
    return discussion_list"""