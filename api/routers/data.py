from fastapi import APIRouter
from database.data.crud import Crud

router_data = APIRouter(tags=["Data"])


@router_data.get("/sale/today")
async def sales_today():
    try:
        db =  Crud()
        response = db.sales_today()
        if response:
            return response
    except Exception as e:
        return e
    

@router_data.get("/sale/especific")
async def sales_especific_day(date: str):
    try:
        db =  Crud()
        response = db.sales_by_date(target_date=date)
        if response:
            return response
    except Exception as e:
        return e

