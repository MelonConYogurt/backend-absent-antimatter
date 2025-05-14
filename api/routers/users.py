from fastapi import APIRouter, HTTPException
from ..models.users.user import User
from database.users.crud import Crud
from models.response_model import Response


router_users = APIRouter(tags=["Users"])


@router_users.get("/users/list-filtered/")
async def search_users(
    offset: int = 0,
    limit: int = 20,
    order_direction: str | None = "ASC",
    search_value: str | None = None,
    column: str | None = "id",
):
    try:
        db = Crud()
        response = db.search_user(
            offset=offset,
            limit=limit,
            order_direction=order_direction,
            search_value=search_value,
            column=column,
        )
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        return response
    except Exception as e:
        return Response(success=False, error=str(e))


@router_users.post("/users/create/")
async def create_user(user_data: User):
    try:
        db = Crud()
        response = db.create_user(data=user_data)
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        return response
    except Exception as e:
        return Response(success=False, error=str(e))


@router_users.delete("/users/delete-by-id/")
async def delete_user(user_id: int):
    try:
        db = Crud()
        response = db.delete_user(user_id=user_id)
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        return response
    except Exception as e:
        return Response(success=False, error=str(e))


@router_users.put("/users/update-info/")
async def update_user(user_data: User):
    try:
        db = Crud()
        response = db.update_user(data=user_data)
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        return response
    except Exception as e:
        return Response(success=False, error=str(e))


@router_users.patch("/users/toggle-active-state/")
async def toggle_user_state(user_data: User):
    try:
        db = Crud()
        response = db.change_user_active_state(data=user_data)
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        return response
    except Exception as e:
        return Response(success=False, error=str(e))


@router_users.post("/users/generate-demo-users/")
async def create_fake_users():
    try:
        db = Crud()
        response = db.create_fake_users()
        if response:
            return response
    except Exception as e:
        return e
