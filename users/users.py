from fastapi import APIRouter
from users.models import UserCreate
from users.utils import create_user, get_user_data

users_router = APIRouter()

@users_router.post("/api/authenticate", response_model=UserCreate)
def authenticate_user(user_data: UserCreate):
    #return {"created": True}
    user = get_user_data(user_data)
    if not user:
        user = create_user(user_data)
    return user
