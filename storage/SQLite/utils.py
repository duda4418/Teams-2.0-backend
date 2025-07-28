from storage.SQLite.db_models import User, Discussion, Message

def create_user(session, name, password, user_id):
    obj = User(name=name, password=password, id=user_id)
    session.add(obj)
    session.commit()
    return obj

def get_users(session):
    users = session.query(User).all()
    return User.serialize_users(users)

def create_discussion(session, contacts, discussion_id):
    obj = Discussion(contacts=contacts, id=discussion_id)
    session.add(obj)
    session.commit()
    return obj

def add_to_group_chat(session, discussion_id, contacts):
    obj = session.query(Discussion).filter(Discussion.id == discussion_id).update({'contacts': contacts})
    session.commit()
    return obj

def get_discussions(session):
    discussions = session.query(Discussion).all()
    return Discussion.serialize_discussions(discussions)

def create_message(session, message_id, discussion_id, user_id, time, value):
    obj = Message(id=message_id, discussion_id=discussion_id, user_id=user_id, time=time, value=value)
    session.add(obj)
    session.commit()
    return obj

def get_messages(session):
    messages = session.query(Message).all()
    return Message.serialize_messages(messages)
