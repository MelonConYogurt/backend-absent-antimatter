from fastapi import APIRouter, HTTPException
from database.sales.crud import Crud
from models.response_model import Response
from typing import List
from ..models.products.sale_products import SaleProduct, Sale

router_sales = APIRouter(tags=["Sales"])


@router_sales.post("/sale/products/")
async def test(products: List[SaleProduct], client_id: int, user_id: int):
    try:
        db = Crud()
        response = db.sale_products(
            products=products, client_id=client_id, user_id=user_id
        )
        if response.success:
            return response
        else:
            raise HTTPException(status_code=400, detail=response.error or "Sale failed")
    except Exception as e:
        return Response(success=False, error=str(e))


@router_sales.get("/sales/")
async def get_sales(
    limit: int = 10,
    offset: int = 0,
    search_value: str | None = None,
    order_direction: str | None = "ASC",
    column: str | None = "id",
):
    try:
        db = Crud()
        response = db.get_sales(
            limit=limit,
            offset=offset,
            column=column,
            search_value=search_value,
            order_direction=order_direction,
        )
        if response.success:
            return response
        else:
            raise HTTPException(status_code=400, detail=response.error or "Sale failed")
    except Exception as e:
        return Response(success=False, error=str(e))
