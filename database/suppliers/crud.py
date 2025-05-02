from database.connection import Connection
from models.response_model import Response, Metadata
from models.supplier_model import Supplier
from faker import Faker
from faker_e164.providers import E164Provider


class Crud:
    def __init__(self):
        self.connection = Connection()

    def validate_supplier(self, id: int):
        try:
            with self.connection.conn() as conn:
                with conn.cursor() as cur:
                    query = "SELECT * FROM public.suppliers WHERE id = %s"
                    cur.execute(query, (id,))
                    response = cur.fetchone()
                    if response:
                        return Response(success=True)
                    else:
                        return Response(success=False)
        except Exception as e:
            return Response(success=False, error=str(e))

    def create_supplier(self, data: Supplier):
        try:
            with self.connection.conn() as conn:
                with conn.cursor() as cur:
                    exist = self.validate_supplier(data.id)
                    if exist.success:
                        query = "INSERT INTO public.suppliers (name, phone, email, address, active) VALUES (%s, %s, %s, %s, %s)"
                        cur.execute(
                            query,
                            (
                                data.name,
                                data.phone,
                                data.email,
                                data.address,
                                data.active,
                            ),
                        )
                        conn.commit()
                        return Response(success=True)
        except Exception as e:
            return Response(success=False, error=str(e))

    def create_fake_suppliers(self):
        try:
            fake = Faker()
            for _ in range(10):
                supplier = Supplier(
                    name=fake.company(),
                    phone=fake.e164()
                    email=fake.company_email(),
                    address=fake.address(),
                    active=True,
                )

                self.create_supplier(supplier)
        except Exception as e:
            return Response(success=False, error=str(e))

    def search_supplier(self):
        try:
            with self.connection.conn() as conn:
                with conn.cursor() as cur:
                    query = "SELECT * FROM public.suppliers"
                    cur.execute(query)
                    data = cur.fetchall()
                    if data:
                        return Response(success=True, data=data)

        except Exception as e:
            return Response(success=False, error=str(e))
