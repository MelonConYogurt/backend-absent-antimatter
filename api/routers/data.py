from fastapi import APIRouter, HTTPException
from database.data.crud import Crud

router_data = APIRouter(tags=["Data"])


@router_data.get("/sales/today/")
async def get_daily_sales_total():
    try:
        db =  Crud()
        response = db.sales_today()
        if response.success:
            return response
        else:
            raise HTTPException(status_code=404, detail='No sales data found for today')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Internal server error: {str(e)}')
    

@router_data.get("/sales/by-date/")
async def get_sales_total_by_date(date: str):
    try:
        if not date:
            raise HTTPException(status_code=400, detail='Date parameter is required')
        
        db =  Crud()
        response = db.sales_by_date(target_date=date)
        if response.success:
            return response
        else:
            raise HTTPException(status_code=404, detail=f'No sales data found for date: {date}')
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f'Invalid date format: {str(e)}')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Internal server error: {str(e)}')


@router_data.get("/sales/monthly/")
async def get_monthly_sales_total(date: str | None = None):
    try:
        db =  Crud()
        response = db.sales_by_month(input_date=date)
        if response.success:
            return response
        else:
            raise HTTPException(status_code=404, detail='No monthly sales data found')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Internal server error: {str(e)}')


@router_data.get("/products/best-selling/")
async def get_top_selling_products():
    try:
        db = Crud()
        response = db.top_10_best_selling_products()
        if response.success:
            return response
        else:
            raise HTTPException(status_code=404, detail='No best-selling products data found')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Internal server error: {str(e)}')

@router_data.get("/inventory/total-value/")
async def get_total_inventory_value():
    try:
        db = Crud()
        response = db.total_inventory_value()
        if response.success:
            return response
        else:
            raise HTTPException(status_code=404, detail='No inventory data found')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Internal server error: {str(e)}')
    
    
@router_data.get("/products/low-stock")
async def get_low_stock_products():
    try:
        db = Crud()
        response = db.get_products_in_low_stock()
        if response.success:
            return response
        else:
            raise HTTPException(status_code=404, detail='No products` data found')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Internal server error: {str(e)}')