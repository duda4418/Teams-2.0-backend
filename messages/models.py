from typing import Optional

from pydantic import BaseModel


class Messages(BaseModel):
    id: Optional[str] = None
    discussion_id: str
    user_id: str
    value: str