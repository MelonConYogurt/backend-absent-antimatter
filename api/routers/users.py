from fastapi import APIRouter, HTTPException
from api.models.users.user import (
    UserBase,
    UserUpdate,
    UserDelete,
    UserResponse,
)
from database.users.crud import Crud
from models.response_model import Response


router_users = APIRouter(tags=["Users"])


@router_users.get("/users/search/")
async def search_users(
    search: str | None = None,
    offset: int = 0,
    limit: int = 100,
):
    try:
        db = Crud()
        response = db.search_user(
            search_value=search,
            offset=offset,
            limit=limit,
        )
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        return response
    except Exception as e:
        return Response(success=False, error=str(e))


@router_users.post("/users/")
async def create_user(user_data: UserBase):
    try:
        db = Crud()
        response = db.create_user(data=user_data)
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        return response
    except Exception as e:
        return Response(success=False, error=str(e))


@router_users.delete("/users/delete/")
async def delete_user(user_id: int):
    try:
        db = Crud()
        response = db.delete_user(data=UserDelete(id=user_id))
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        return response
    except Exception as e:
        return Response(success=False, error=str(e))


@router_users.put("/users/update/")
async def update_user(user_data: UserUpdate):
    try:
        db = Crud()
        response = db.update_user(data=user_data)
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        return response
    except Exception as e:
        return Response(success=False, error=str(e))


@router_users.patch("/users/change/state/")
async def change_active_state(user_data: UserResponse):
    try:
        db = Crud()
        response = db.change_user_active_state(data=user_data)
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        return response
    except Exception as e:
        return Response(success=False, error=str(e))


@router_users.post("/create/fake/users/")
async def create_fake_users():
    try:
        db = Crud()
        response = db.create_fake_users()
        if response:
            return response
    except Exception as e:
        return e
