from collections import deque

from messages.utils import get_messages_by_discussion_id
from openAI.models import OpenAIChat


def append_to_history(discussion_id, message):
    message_list = get_messages_by_discussion_id(discussion_id)

    normalized_messages = [
        {"role": msg.get("role", "user"), "content": msg.get("value", "")}
        for msg in message_list
    ]

    recent_messages = normalized_messages[-9:]

    developer_prompt = {"role": "developer", "content": "You are a helpful assistant."}

    history = [developer_prompt] + recent_messages

    normalized_new_message = {
        "role": "user",
        "content": message
    }
    history.append(normalized_new_message)

    return history

def process_message_with_history(discussion_id, message, client):
    instructions: str = "Keep your answers simple and concise. "

    chat_history = append_to_history(discussion_id, message)
    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=instructions,
        input= list(chat_history),
        max_output_tokens = 500,
        store = False
    )
    return  response.output[0].content[0].text