from fastapi import APIRouter, HTTPException
from database.sales.crud import Crud
from models.response_model import Response
from typing import List
from ..models.products.sale_products import SaleProduct


router_sales = APIRouter(tags=["Sales"])


@router_sales.post("/test/")
async def test(products: List[SaleProduct]):
    try:
        db = Crud()
        response = db.sale_products(products=products)
        if response.success:
            return response
    except Exception as e:
        return Response(success=False, error=str(e))
