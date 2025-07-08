from fastapi import APIRouter, HTTPException
from database.sales.crud import Crud
from database.clients.crud import Crud as ClientCrud
from database.users.crud import Crud as UserCrud
from database.products.crud import Crud as ProductCrud
from models.response_model import Response
from models.sale_product import Product
from typing import List
from faker import Faker
import random
from ..models.products.sale_products import SaleProduct

router_sales = APIRouter(tags=["Sales"])
fake = Faker()


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


@router_sales.delete("/sales/delete/")
async def delete_sale(id: int):
    try:
        db = Crud()
        response = db.delete_sale(id=id)

        if response.success:
            return response
        else:
            raise HTTPException(status_code=400, detail=response.error or "Sale failed")
    except Exception as e:
        return Response(success=False, error=str(e))


@router_sales.post("/sales/generate/")
async def generate_fake_sales(count: int = 10):
    """
    Genera ventas falsas usando datos reales de la base de datos
    """
    try:
        # Obtener IDs reales de clientes, usuarios y productos
        client_crud = ClientCrud()
        user_crud = UserCrud()
        product_crud = ProductCrud()

        # Obtener clientes activos
        clients_response = client_crud.search_client(limit=100, offset=0)
        if not clients_response.success or not clients_response.data:
            raise HTTPException(status_code=400, detail="No hay clientes disponibles")

        # Obtener usuarios activos
        users_response = user_crud.search_user(limit=100, offset=0)
        if not users_response.success or not users_response.data:
            raise HTTPException(status_code=400, detail="No hay usuarios disponibles")

        # Obtener productos activos con stock
        products_response = product_crud.search_products(limit=200, offset=0)
        if not products_response.success or not products_response.data:
            raise HTTPException(status_code=400, detail="No hay productos disponibles")

        # Filtrar solo productos con stock > 0
        available_products = [p for p in products_response.data if p.stock > 0]
        if not available_products:
            raise HTTPException(status_code=400, detail="No hay productos con stock disponible")

        client_ids = [client.id for client in clients_response.data]
        user_ids = [user.id for user in users_response.data]

        generated_sales = []
        sales_crud = Crud()

        for _ in range(count):
            # Seleccionar cliente y usuario aleatorios
            client_id = random.choice(client_ids)
            user_id = random.choice(user_ids)

            # Generar entre 1 y 5 productos por venta
            num_products = random.randint(1, min(5, len(available_products)))
            selected_products = random.sample(available_products, num_products)

            # Crear lista de productos para la venta
            sale_products = []
            for product in selected_products:
                # Cantidad aleatoria entre 1 y el stock disponible (máximo 10)
                max_quantity = min(product.stock, 10)
                quantity = random.randint(1, max_quantity)

                sale_products.append(Product(id=product.id, quantity=quantity, price=product.price))

            # Crear la venta
            response = sales_crud.sale_products(
                products=sale_products,
                client_id=client_id,
                user_id=user_id,
            )

            if response.success:
                generated_sales.append(
                    {
                        "client_id": client_id,
                        "user_id": user_id,
                        "products": len(sale_products),
                        "total": response.data.get("total", 0) if response.data else 0,
                    }
                )
            else:
                print(f"Error generando venta: {response.error}")

        return Response(
            success=True,
            data={"generated_sales": len(generated_sales), "sales": generated_sales},
        )

    except Exception as e:
        return Response(success=False, error=str(e))

