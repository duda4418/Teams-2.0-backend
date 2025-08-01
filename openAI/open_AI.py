import os
from fastapi import APIRouter, HTTPException
from openai import OpenAI

from messages.models import Messages
from messages.utils import create_new_message
from openAI.models import OpenAIChat
from openAI.utils import process_message_with_history
from storage.SQLite.real_db import db
from websocket_manager.manager import ConnectionManager

openai_router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@openai_router.post("/api/openai", response_model=OpenAIChat)
async def create_openai_response(request_data: OpenAIChat):
    discussion_id = request_data.discussion_id
    user_id = request_data.user_id
    user_message = request_data.user_message

    # Validate discussion
    discussion = db.get_discussions().get(discussion_id)
    if not discussion:
        raise HTTPException(status_code=404, detail="Discussion not found")

    discussion_contacts = discussion.get("contacts", [])
    if user_id not in discussion_contacts:
        raise HTTPException(status_code=403, detail="User not part of the discussion")

    message_data = Messages(
        id=None,
        discussion_id=discussion_id,
        user_id=user_id,
        value=user_message
    )
    message_dict = create_new_message(message_data)
    message_dict["type"] = "message"

    connection_manager = ConnectionManager()
    await connection_manager.broadcast(message_dict, discussion_contacts)

    response = process_message_with_history(discussion_id, user_message, client)

    message_data = Messages(
        id=None,
        discussion_id= discussion_id,
        user_id="6fd8304c-0e5e-4952-92e0-6214d06e675c", # OpenAI bot user ID
        value=response
    )
    message_dict = create_new_message(message_data)
    message_dict["type"] = "message"

    await connection_manager.broadcast(message_dict, discussion_contacts)

    return OpenAIChat(
        id=message_data.id,
        discussion_id=message_data.discussion_id,
        user_id=message_data.user_id,
        user_message=message_data.value,
        image=None,
        audio=None
    )
