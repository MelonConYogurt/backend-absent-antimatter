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

    def create_fake_products(self):
        try:
            fake = Faker()

            for _ in range(20):
                product_name = fake.word().capitalize() + " " + fake.word()
                stock = fake.random_int(min=5, max=100)
                reference = fake.bothify(text="???-####")
                category_id = fake.random_int(min=4, max=10)
                price = fake.pydecimal(left_digits=3, right_digits=2, positive=True)
                supplier_id = fake.random_int(min=4, max=10)

                product = Product(
                    name=product_name,
                    stock=stock,
                    reference=reference,
                    category_id=category_id,
                    price=price,
                    supplier_id=supplier_id,
                )
                response = self.create_product(data=product)
                print(
                    f"Product creation success: {response.success}, Product data: {product}, error: {response.error}"
                )

            return Response(success=True)
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

    def search_products(
        self,
        offset: int,
        limit: int,
        order_direction: str | None = "ASC",
        search_value: str | None = None,
        column: str | None = "id",
    ):
        VALID_COLS = {
            "id",
            "name",
            "stock",
            "reference",
            "category_id",
            "price",
            "created_at",
            "supplier_id",
            "active",
        }
        VALID_ORDERS = {"ASC", "DESC"}

        column = column if column in VALID_COLS else "id"
        order_direction = order_direction if order_direction in VALID_ORDERS else "ASC"

        order_clause = f"ORDER BY {column} {order_direction}"

        try:
            with self.connection.conn() as conn:
                with conn.cursor() as cur:
                    query = f"""
                    SELECT *
                    FROM public.products
                    WHERE name ILIKE %s OR reference ILIKE %s
                    {order_clause}
                    LIMIT %s OFFSET %s
                    """
                    like_pattern = f"%{search_value or ''}%"
                    cur.execute(query, (like_pattern, like_pattern, limit, offset))
                    rows = cur.fetchall()

                    if rows:
                        query_total_rows = """
                        SELECT COUNT(*)
                        FROM public.products
                        WHERE name ILIKE %s OR reference ILIKE %s
                        """
                        cur.execute(query_total_rows, (like_pattern, like_pattern))
                        total = cur.fetchone()[0]
                        page = offset // limit + 1

                        return Response(
                            success=True,
                            data=[
                                Product(
                                    id=row[0],
                                    name=row[1],
                                    stock=row[2],
                                    reference=row[3],
                                    category_id=row[4],
                                    price=row[5],
                                    created_at=row[6],
                                    supplier_id=row[7],
                                    active=row[8],
                                )
                                for row in rows
                            ],
                            metadata=Metadata(page=page, total=total, size=limit),
                        )
                    else:
                        return Response(
                            success=False,
                        )
        except Exception as e:
            return Response(success=False, error=str(e))
