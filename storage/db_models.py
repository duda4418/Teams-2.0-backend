import uuid
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, ARRAY, UUID, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class User(Base):

    __tablename__ = 'User'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)

    @staticmethod
    def serialize_users(users):
        serialized_users = {}
        for user in users:
            serialized_users[str(user.id)] = {
                "id": str(user.id),
                "name": str(user.name),
                "password": str(user.password)
            }
        return serialized_users

class Discussion(Base):
    __tablename__ = 'Discussion'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    contacts = Column(ARRAY(UUID(as_uuid=True)), nullable=False)
    name = Column(String, nullable=True)

    @staticmethod
    def serialize_discussions(discussions):
        serialized_discussions = {}
        for discussion in discussions:
            serialized_contacts = [str(contact) for contact in discussion.contacts]
            serialized_discussions[str(discussion.id)] = {
                "id": str(discussion.id),
                "contacts": serialized_contacts,
                "name": str(discussion.name)
            }
        return serialized_discussions

class Message(Base):
    __tablename__ = 'Message'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    discussion_id = Column(UUID(as_uuid=True), ForeignKey("Discussion.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("User.id"), nullable=False)
    value = Column(String, nullable=False)
    time = Column(DateTime, default=datetime.utcnow)

    @staticmethod
    def serialize_messages(messages):
        serialized_messages = {}
        for message in messages:
            serialized_messages[str(message.id)] = {
                "id": str(message.id),
                "discussion_id": str(message.discussion_id),
                "user_id": str(message.user_id),
                "value": str(message.value),
                "time": str(message.time),
            }
        return serialized_messages

