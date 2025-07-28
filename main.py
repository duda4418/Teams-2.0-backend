from fastapi import FastAPI

from contacts.contacts import contacts_router
from discussions.discussions import discussions_router
from messages.messages import message_router
from users.users import users_router
from starlette.websockets import WebSocket, WebSocketDisconnect
from websocket_manager.manager import ConnectionManager
from websocket_manager.status import status_router

app = FastAPI()
app.include_router(users_router)
app.include_router(contacts_router)
app.include_router(discussions_router)
app.include_router(message_router)
app.include_router(status_router)

websocket_manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websockets_endpoint(websocket: WebSocket, client_id: str):
    await websocket_manager.connect(websocket, client_id)
    try:
        while True:
            message = await websocket.receive_text()
    except WebSocketDisconnect:
        await websocket_manager.disconnect(websocket, client_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port = 8000)