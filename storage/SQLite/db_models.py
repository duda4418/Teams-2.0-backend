import uuid
import json
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TypeDecorator

Base = declarative_base()

# Custom type for JSON list storage (replacing ARRAY for SQLite)
class JSONEncodedList(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return "[]"
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return []
        return json.loads(value)

class User(Base):
    __tablename__ = 'User'
    id = Column(String, primary_key=True, nullable=False, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)

    @staticmethod
    def serialize_users(users):
        return {
            str(user.id): {
                "id": str(user.id),
                "name": user.name,
                "password": user.password
            } for user in users
        }

class Discussion(Base):
    __tablename__ = 'Discussion'
    id = Column(String, primary_key=True, nullable=False, default=lambda: str(uuid.uuid4()))
    contacts = Column(JSONEncodedList, nullable=False)
    name = Column(String, nullable=True)

    @staticmethod
    def serialize_discussions(discussions):
        return {
            str(discussion.id): {
                "id": str(discussion.id),
                "contacts": discussion.contacts,
                "name": discussion.name
            } for discussion in discussions
        }

class Message(Base):
    __tablename__ = 'Message'
    id = Column(String, primary_key=True, nullable=False, default=lambda: str(uuid.uuid4()))
    discussion_id = Column(String, ForeignKey("Discussion.id"), nullable=False)
    user_id = Column(String, ForeignKey("User.id"), nullable=False)
    value = Column(String, nullable=False)
    time = Column(DateTime, default=datetime.utcnow)

    @staticmethod
    def serialize_messages(messages):
        return {
            str(message.id): {
                "id": str(message.id),
                "discussion_id": str(message.discussion_id),
                "user_id": str(message.user_id),
                "value": message.value,
                "time": str(message.time),
            } for message in messages
        }
