from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from storage.SQLite.db_models import User, Discussion, Message, Base
from storage.SQLite.utils import get_users, get_discussions, get_messages, create_user, create_discussion, create_message

engine = create_engine(
    'sqlite:///./chat_app_database.db',  # ✅ Switched from PostgreSQL to SQLite
    echo=True,
    connect_args={"check_same_thread": False}  # Required for SQLite multithreading with SQLAlchemy
)

Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

class Database:
    def __init__(self):
        self.db = {
            "users": self.get_users(),
            "discussions": self.get_discussions(),
            "messages": self.get_messages()
        }

    @staticmethod
    def create_user(name, password, user_id):
        return create_user(session=session, name=name, password=password, user_id=user_id)

    @staticmethod
    def get_users():
        return get_users(session=session)

    @staticmethod
    def create_discussion(contacts, discussion_id):
        return create_discussion(session=session, contacts=contacts, discussion_id=discussion_id)

    @staticmethod
    def get_discussions():
        return get_discussions(session=session)

    @staticmethod
    def create_message(message_id, discussion_id, user_id, time, value):
        return create_message(
            session=session,
            message_id=message_id,
            discussion_id=discussion_id,
            user_id=user_id,
            time=time,
            value=value
        )

    @staticmethod
    def get_messages():
        return get_messages(session=session)

db = Database()