from fastapi import APIRouter, HTTPException
from api.models.clients import *
from database.clients.crud import Crud
from models.response_model import Response


router_clients = APIRouter(tags=["Clients"])


@router_clients.get("/clients/list-filtered/")
async def search_clients(
    limit: int = 20,
    offset: int = 0,
    order_direction: str | None = "ASC",
    search_value: str | None = None,
    column: str | None = "id",
):
    try:
        db = Crud()
        response = db.search_client(
            limit=limit,
            offset=offset,
            search_value=search_value,
            order_direction=order_direction,
            column=column,
        )
        if not response.success:
            raise HTTPException(status_code=404, detail=response.error)
        else:
            return response
    except Exception as e:
        return Response(error=str(e))


@router_clients.patch("/clients/toggle-active-state/")
async def toggle_client_state(id: int):
    try:
        db = Crud()
        response = db.delete_client(id=id)
        if not response.success:
            raise HTTPException(status_code=404, detail=response.error)
        else:
            return response
    except Exception as e:
        return Response(error=str(e))


@router_clients.post("/clients/generate-demo-clients/")
async def create_fake_clients():
    try:
        db = Crud()
        db.create_fake_clients()
    except Exception as e:
        return Response(error=str(e))
