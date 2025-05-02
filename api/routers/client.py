from fastapi import APIRouter
from api.models.clients import *
from database.clients.crud import Crud
from models.response_model import Response


router_clients = APIRouter(tags=["Clients"])


@router_clients.get("/clients/search/")
async def search_clients(limit: int, offset: int, search_value: str | None = None):
    try:
        db = Crud()
        response = db.search_client(
            limit=limit, offset=offset, search_value=search_value
        )
        return response
    except Exception as e:
        return Response(error=str(e))


@router_clients.patch("/clients/toggle-active/")
async def toggle_client_active(id: int):
    try:
        db = Crud()
        response = db.delete_client(id=id)
        return response
    except Exception as e:
        return Response(error=str(e))


@router_clients.get("/clients/create/fake/")
async def create_clients():
    try:
        db = Crud()
        db.create_fake_clients()
    except Exception as e:
        return Response(error=str(e))
