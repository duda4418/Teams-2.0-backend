# Teams 2.0 backend
Creating the API Server for chat_app

## Overview
This repository provides the backend API server for a chat application, designed to enable real-time messaging and group communication. Built with FastAPI and leveraging PostgreSQL for data storage, the solution offers robust user authentication, contact management, discussion (chat) creation, and message handling via both RESTful endpoints and WebSocket connections for live updates.

## Solution Architecture

- **Users & Authentication:**  
  Users can register and authenticate. User data, including credentials, are securely stored and managed in the database. Authentication endpoints ensure only valid users can access chat features.

- **Contacts:**  
  The backend exposes endpoints to fetch all users or individual contacts by ID, supporting the display of contact lists within clients.

- **Discussions (Chats):**  
  Supports both one-to-one and group discussions. Each discussion records its participating contacts and an optional name. The API prevents duplicate discussions and provides endpoints to create or list existing chats for a user, with user-friendly naming logic for one-to-one and self-chats.

- **Messages:**  
  Users can send messages within discussions. Each message is associated with a user, discussion, timestamp, and content. Messages are serialized and stored in the database. The API allows posting and retrieving messages per discussion.

- **WebSocket Support:**  
  Real-time communication is enabled through WebSockets, allowing clients to receive instant updates—ideal for chat message delivery and presence notifications.

- **Database Layer:**  
  Utilizes SQLAlchemy ORM models for `User`, `Discussion`, and `Message` entities. All core operations (create/query users, discussions, messages) are abstracted through utility and database classes, ensuring clean separation of concerns and maintainability.

## Key Technologies

- **FastAPI** for high-performance API endpoints and WebSocket integration.
- **SQLAlchemy** for ORM-based database access and migrations.
- **PostgreSQL** as the primary relational data store.
- **SQLite** as the second relational data store.

- **Python 3.10+** as the programming language.

## Typical Usage Flow

1. **User Authentication:** Users register or log in.
2. **Contact Management:** Users fetch contacts to initiate conversations.
3. **Chat Creation:** Users create new discussions (one-to-one or group); duplicate prevention logic ensures unique chats.
4. **Messaging:** Users send and receive messages in real time via REST or WebSocket.
5. **Persistence:** All entities (users, discussions, messages) are stored and queried from PostgreSQL.
