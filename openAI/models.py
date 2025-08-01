from pydantic import BaseModel
from typing import Optional

class OpenAIChat(BaseModel):
    id: Optional[str] = None
    discussion_id: str
    user_id: str
    user_message: str
    image: Optional[str] = None
    audio: Optional[str] = None
