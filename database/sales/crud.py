from database.connection import Connection
from models.response_model import Response, Metadata
from models.sale_model import Sale
from models.sale_product import SaleProduct
from typing import List
from faker import Faker


class Crud:
    def __init__(self):
        self.connection = Connection()

    def generade_sale(self, data: Sale):
        try:
            with self.connection.conn() as conn:
                with conn.cursor() as cur:
                    query = "INSERT INTO public.sales (client_id, user_id, total) VALUES (%s, %s, %s) RETURNING id"
                    cur.execute(query, (data.client_id, data.user_id, data.total))
                    sale_id = cur.fetchone()[0]
                    return Response(success=True, data={"id": sale_id})

        except Exception as e:
            return Response(success=False, error=str(e))

    def validate_product(self, id: int, quantity: int):
        try:
            with self.connection.conn() as conn:
                with conn.cursor() as cur:
                    query = "SELECT stock FROM public.products WHERE id = %s"
                    cur.execute(query, (id,))
                    stock = cur.fetchone()[0]

                    if quantity > stock:
                        return Response(success=False, data={"stock": stock})
                    else:
                        return Response(success=True, data={"stock": stock})
        except Exception as e:
            return Response(success=False, error=str(e))

    def sale_products(self, products: List[SaleProduct]):
        try:
            with self.connection.conn() as conn:
                with conn.cursor() as cur:
                    total = 0
                    for product in products:
                        validation = self.validate_product(
                            id=product.id, quantity=product.quantity
                        )
                        if validation.success:
                            total += product.quantity * product.price
                        else:
                            raise Exception
                    return Response(success=True, data={"total": total})
        except Exception as e:
            return Response(success=False, error=str(e))
