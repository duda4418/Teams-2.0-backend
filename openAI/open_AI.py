import os
from fastapi import APIRouter, HTTPException
from openai import OpenAI
from openAI.models import OpenAIChat
from openAI.utils import process_message_with_history
from storage.SQLite.real_db import db

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

    response = process_message_with_history(discussion_id, user_message, client)
    return {
        "id": None,
        "discussion_id": discussion_id,
        "user_id": user_id,
        "user_message": response,
        "image": None,
        "audio": None
    }
    # try:
    #     # Build context from discussion history
    #     all_messages = db.get_messages().values()
    #     discussion_history = [msg for msg in all_messages if msg["discussion_id"] == discussion_id]
    #
    #     # Sort messages by time using itemgetter
    #     discussion_history = sorted(discussion_history, key=itemgetter("time"))
    #
    #     # Build OpenAI message format
    #     messages = [{"role": "system", "content": "You are a helpful assistant."}]
    #     for msg in discussion_history:
    #         role = "assistant" if msg["user_id"] == "openai_bot" else "user"
    #         messages.append({
    #             "role": role,
    #             "content": msg["value"]
    #         })
    #
    #     # Add the current user message
    #     messages.append({"role": "user", "content": user_message})
    #
    #     # Get GPT response
    #     response = client.chat.completions.create(
    #         model="gpt-4.1",
    #         messages=messages
    #     )
    #     bot_response = response.choices[0].message.content
    #
    #     # Build new message record
    #     message_id = str(uuid4())
    #     now = datetime.now()
    #
    #     message_dict = {
    #         "id": message_id,
    #         "discussion_id": discussion_id,
    #         "user_id": "openai_bot",
    #         "value": bot_response,
    #         "time": now.isoformat(),
    #         "type": "message"
    #     }
    #
    #     # Save to DB
    #     db.create_message(
    #         message_id=message_id,
    #         discussion_id=discussion_id,
    #         user_id="openai_bot",
    #         value=bot_response,
    #         time=now
    #     )
    #
    #     # Broadcast
    #     connection_manager = ConnectionManager()
    #     await connection_manager.broadcast(message_dict, discussion_contacts)
    #
    #     return OpenAIChat(
    #         discussion_id=discussion_id,
    #         user_id=user_id,
    #         user_message=bot_response
    #     )
    #
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
