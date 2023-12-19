from fastapi import APIRouter
from websocket_manager.manager import ConnectionManager

status_router = APIRouter()

@status_router.post("/api/status")
def set_status():
    connection_manager = ConnectionManager()
    connection_manager.status()