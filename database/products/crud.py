from database.connection import Connection
from models.response_model import Response, Metadata
from models.product_model import Product
from models.category_model import Category
from faker import Faker


class Crud:
    def __init__(self):
        self.connection = Connection()

    def validate_category(self, id: int):
        try:
            with self.connection.conn() as conn:
                with conn.cursor() as cur:
                    query = "SELECT * FROM public.categories WHERE id = %s"
                    cur.execute(query, (id,))
                    response = cur.fetchone()
                    if response is None:
                        return Response(success=False)
                    else:
                        return Response(success=True)
        except Exception as e:
            return Response(success=False, error=str(e))

    def create_category(self, data: Category):
        try:
            with self.connection.conn() as conn:
                with conn.cursor() as cur:
                    check_query = "SELECT id FROM public.categories WHERE name = %s"
                    cur.execute(check_query, (data.name,))
                    exists = cur.fetchone()
                    if exists:
                        return Response(
                            success=False,
                            error=f"Ya existe una categoría con este nombre: {data.name}",
                        )

                    query = (
                        "INSERT INTO public.categories (name) VALUES (%s) RETURNING id"
                    )
                    cur.execute(query, (data.name,))
                    response = cur.fetchone()[0]
                    if not response:
                        return Response(success=False)
                    else:
                        return Response(success=True)

        except Exception as e:
            return Response(success=False, error=str(e))

    def search_categories(self):
        try:
            with self.connection.conn() as conn:
                with conn.cursor() as cur:
                    query = "SELECT * FROM public.categories"
                    cur.execute(query)
                    data = cur.fetchall()
                    if data:
                        return Response(
                            success=True,
                            data=[
                                Category(id=category[0], name=category[1])
                                for category in data
                            ],
                        )
                    else:
                        return Response(success=False)
        except Exception as e:
            return Response(success=False, error=str(e))

    def create_fake_categories(self):
        try:
            fake = Faker()

            for _ in range(10):
                category_name = fake.word().capitalize()
                category = Category(name=category_name)
                self.create_category(data=category)

            return Response(
                success=True,
            )
        except Exception as e:
            return Response(success=False, error=str(e))

    def create_product(self, data: Product):
        try:
            with self.connection.conn() as conn:
                with conn.cursor() as cur:
                    query = """
                        INSERT INTO public.products 
                        (name, stock, reference, category_id, price, supplier_id) 
                        VALUES (%s, %s, %s, %s, %s, %s) 
                        RETURNING id
                    """
                    cur.execute(
                        query,
                        (
                            data.name,
                            data.stock,
                            data.reference,
                            data.category_id,
                            data.price,
                            data.supplier_id,
                        ),
                    )
                    response = cur.fetchone()[0]
                    if not response:
                        return Response(success=False)
                    else:
                        return Response(success=True, data={"product_id": response})

        except Exception as e:
            return Response(success=False, error=str(e))
