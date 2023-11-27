from fastapi import APIRouter, HTTPException

from messages.models import Messages
from messages.utils import create_new_message, get_messages_by_discussion_id
from storage.fake_db import fake_db
from websocket_manager.manager import ConnectionManager

message_router = APIRouter()

@message_router.post("/api/messages", response_model=Messages)
async def create_message(message_data: Messages):

    discussion_id = message_data.discussion_id
    user_id = message_data.user_id

    discussion = fake_db.get("discussions", {}).get(discussion_id)
    if not discussion:
        raise HTTPException(status_code=404, detail="Discussion not found")

    discussion_contacts = discussion.get("contacts", [])
    if user_id not in discussion_contacts:
        raise HTTPException(status_code=404, detail="No user part in conversation")

    message_dict = create_new_message(message_data)
    message_dict["type"] = "message"
    #fake_db.create_message(message_data)

    connection_manager = ConnectionManager()
    await connection_manager.broadcast(message_dict, discussion_contacts)

    return message_data

@message_router.get("/api/messages")
def get_message(user_id: str, discussion_id: str):

    discussion = fake_db.get("discussions", {}).get(discussion_id)
    if not discussion:
        raise HTTPException(status_code = 404, detail="Discussion not found")

    discussion_contacts = discussion.get("contacts", [])
    if user_id not in discussion_contacts:
        raise HTTPException(status_code = 404, detail="User is not part of any discussion")

    return get_messages_by_discussion_id(discussion_id)