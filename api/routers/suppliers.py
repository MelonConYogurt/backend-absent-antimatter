from fastapi import APIRouter, HTTPException
from database.suppliers.crud import Crud
from models.response_model import Response

router_suppliers = APIRouter(tags=["Suppliers"])


@router_suppliers.get("/suppliers/")
async def search_suppliers():
    try:
        db = Crud()
        response = db.search_supplier()
        if response.success:  # Corregido: succes -> success
            return response  # Devolver los datos completos
    except Exception as e:
        return Response(success=False, error=str(e))


@router_suppliers.post("/suppliers/create/")
async def create_supplier():
    try:
        db = Crud()
        response = db.create_supplier()
        if response.success:
            return Response(success=True)
    except Exception as e:
        return Response(success=False, error=str(e))


@router_suppliers.post("/suppliers/fake/")
async def create_fake_suppliers():
    try:
        db = Crud()
        response = db.create_fake_suppliers()
        return response
    except Exception as e:
        return Response(success=False, error=str(e))
