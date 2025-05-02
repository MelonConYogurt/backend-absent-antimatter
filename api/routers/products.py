from fastapi import APIRouter, HTTPException
from database.products.crud import Crud

router_products = APIRouter(tags=["Products"])


@router_products.get("/products/")
async def search_products():
    try:
        pass
    except Exception as e:
        print(e)


@router_products.post("/products/categorie/")
async def search_products(name: str):
    try:
        db = Crud()
        response = db.create_categorie(name=name)
        if response:
            return response
    except Exception as e:
        print(e)


@router_products.post("/products/categorie/fake/")
async def search_products():
    try:
        db = Crud()
        response = db.create_fake_categories()
        if response:
            return response
    except Exception as e:
        print(e)
