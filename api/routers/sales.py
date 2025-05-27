from fastapi import APIRouter, HTTPException
from database.sales.crud import Crud
from models.response_model import Response
from typing import List
from ..models.products.sale_products import SaleProduct, Sale

router_sales = APIRouter(tags=["Sales"])


@router_sales.post("/test/")
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
