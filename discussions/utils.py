from collections import Counter
from uuid import uuid4
from storage.real_db import db


def get_contact_discussions(discussion_data):
    discussions = db.get_discussions().values()
    for discussion in discussions:
        contact_id = discussion.get("contacts")
        if Counter(contact_id) == Counter(discussion_data):
            return discussion
    return None

def create_new_discussion(data):
    discussion_id = str(uuid4())
    discussion_data = data.model_dump()
    discussion_data["id"] = discussion_id

    db.create_discussion(contacts=discussion_data["contacts"], discussion_id=discussion_data["id"])

    return discussion_data

def get_discussions(user_id):
    users = db.get_users()
    discussions = db.get_discussions()

    discussions_list = []

    for discussion_key in discussions:
        discussion = discussions[discussion_key]
        contacts = discussion.get("contacts", [])

        one_to_one_discussion = contacts[0] != contacts[1]
        yourself_discussion = contacts[0] == contacts[1]

        if user_id in contacts:
            text = ""
            if one_to_one_discussion:
                for contact in contacts:
                    if user_id != contact:
                        text = text + users.get(contact)["name"] + ", "
                discussion["name"] = text[:-2]
            elif yourself_discussion:
                contact = contacts[0]
                if user_id == contact:
                    discussion["name"] = users.get(contact)["name"]
            discussions_list.append(discussion)
    return discussions_list

def remove_duplicate_contacts(contacts):
    return [contact for index, contact in enumerate(contacts) if contact not in contacts[:index]]