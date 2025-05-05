from fastapi import APIRouter, HTTPException
from database.products.crud import Crud
from models.response_model import Response, Metadata

router_products = APIRouter(tags=["Products"])


@router_products.get("/products/categories/")
async def search_categories():
    try:
        db = Crud()
        response = db.search_categories()
        if response.success:
            return response
    except Exception as e:
        return Response(success=False, error=str(e))


@router_products.post("/products/category/")
async def create_category(name: str):
    try:
        db = Crud()
        response = db.create_category(name=name)
        if response:
            return response
    except Exception as e:
        return Response(success=False, error=str(e))


@router_products.post("/products/category/fake/")
async def create_fake_categories():
    try:
        db = Crud()
        response = db.create_fake_categories()
        if response:
            return response
    except Exception as e:
        return Response(success=False, error=str(e))


@router_products.get("/products/")
async def search_products(
    offset: int,
    limit: int,
    order_direction: str | None = "ASC",
    search_value: str | None = None,
    column: str | None = "id",
):
    try:
        db = Crud()
        response = db.search_products(
            offset=offset,
            limit=limit,
            order_direction=order_direction,
            search_value=search_value,
            column=column,
        )
        if response:
            return response
    except Exception as e:
        return Response(success=False, error=str(e))
