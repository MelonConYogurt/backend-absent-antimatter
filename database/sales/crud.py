from database.connection import Connection
from models.response_model import Response, Metadata
from models.sale_model import Sale
from models.sale_product import SaleProduct, Product
from typing import List


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
                    return Response(success=True, data=sale_id)
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

    def sale_product(self, product: SaleProduct):
        try:
            with self.connection.conn() as conn:
                with conn.cursor() as cur:
                    query_update_product_stock = (
                        "UPDATE public.products SET stock = stock - %s WHERE id = %s"
                    )
                    cur.execute(
                        query_update_product_stock, (product.quantity, product.id)
                    )

                    query_create_product_sale = "INSERT INTO public.sale_products (product_id, sale_id, quantity) VALUES (%s, %s,%s)"
                    cur.execute(
                        query_create_product_sale,
                        (product.id, product.sale_id, product.quantity),
                    )

                    return Response(success=True)

        except Exception as e:
            return Response(success=False, error=str(e))

    def sale_products(self, products: List[Product], client_id: int, user_id: int):
        try:
            total = 0
            for product in products:
                validation = self.validate_product(
                    id=product.id, quantity=product.quantity
                )
                if validation.success:
                    total += product.quantity * product.price
                else:
                    return Response(
                        success=False,
                        error=f"This product dosent have many stock for the sale: {product.id}",
                    )

            if total <= 0:
                return Response(
                    success=False, error="Total of 0, fail in some stock product"
                )
            else:
                sale_id_response = self.generade_sale(
                    data=Sale(client_id=client_id, user_id=user_id, total=total)
                )

                if sale_id_response.data is None:
                    return Response(success=False)
                else:
                    for product in products:
                        self.sale_product(
                            product=SaleProduct(
                                id=product.id,
                                quantity=product.quantity,
                                sale_id=sale_id_response.data,
                            )
                        )
            return Response(success=True, data={"total": total})
        except Exception as e:
            return Response(success=False, error=str(e))

    def get_sales(
        self,
        limit: int,
        offset: int,
        search_value: str | None = None,
        order_direction: str | None = "ASC",
        column: str | None = "id",
    ):
        VALID_COLS = {"id", "client_id", "user_id", "sale_date", "total"}
        VALID_ORDERS = {"ASC", "DESC"}

        order_direction if order_direction in VALID_ORDERS else "ASC"
        column if column in VALID_COLS else "id"

        order_clause = f"ORDER BY {column} {order_direction}"

        try:
            with self.connection.conn() as conn:
                with conn.cursor() as cur:
                    query = f"""
                    SELECT *
                    FROM public.sales
                    WHERE client_id::TEXT ILIKE %s OR user_id::TEXT ILIKE %s
                    {order_clause} 
                    LIMIT %s OFFSET  %s
                    """

                    like_pattren = f"%{search_value or ''}%"

                    cur.execute(query, (like_pattren, like_pattren, limit, offset))
                    sales = cur.fetchall()

                    query_total = """
                                    SELECT COUNT(*)
                                    FROM public.sales
                                    WHERE client_id::TEXT ILIKE %s OR user_id::TEXT ILIKE %s
                                    """
                    cur.execute(query_total, (like_pattren, like_pattren))
                    total = cur.fetchone()[0]

                    page = offset // limit + 1

                    return Response(
                        success=True,
                        data=[
                            Sale(
                                id=sale[0],
                                client_id=sale[1],
                                user_id=sale[2],
                                sale_date=sale[3],
                                total=sale[4],
                            )
                            for sale in sales
                        ],
                        metadata=Metadata(page=page, size=limit, total=total),
                    )

        except Exception as e:
            return Response(success=False, error=str(e))

    def delete_sale(self, id: int):
        try:
            with self.connection.conn() as conn:
                with conn.cursor() as cur:
                    query = "DELETE FROM public.sales WHERE id = %s RETURNING id"
                    cur.execute(query, (id,))
                    response = cur.fetchone()
                    if not response:
                        return Response(success=False)
                    else:
                        return Response(
                            success=True, data={"sale_id_delete:": response[0]}
                        )

        except Exception as e:
            return Response(success=False, error=str(e))
