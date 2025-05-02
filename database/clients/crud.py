from database.connection import Connection
from models.response_model import Response, Metadata
from models.client_model import BaseClient
from faker import Faker
from faker_e164.providers import E164Provider
import psycopg2


class Crud:
    def __init__(self):
        self.connection = Connection()

    def count_total_clients(self):
        try:
            with self.connection.conn() as conn:
                with conn.cursor() as cur:
                    query = "SELECT COUNT(*) FROM public.clients"
                    cur.execute(query)
                    total = cur.fetchone()[0]
                    return total
        except psycopg2.Error as e:
            return 0

    def find_client(self, id: int):
        with self.connection.conn() as conn:
            with conn.cursor() as cur:
                query = "SELECT * FROM public.clients WHERE id = %s"
                cur.execute(query, (id,))
                response = cur.fetchone()
                if not response:
                    return Response(success=False)
                else:
                    return Response(success=True)

    def search_client(self, limit: int, offset: int, search_value: str | None = None):
        try:
            if limit <= 0:
                return Response(
                    success=False, error="El límite debe ser mayor que cero"
                )

            if offset < 0:
                return Response(
                    success=False, error="El offset debe ser mayor o igual a cero"
                )

            with self.connection.conn() as conn:
                with conn.cursor() as cur:

                    if search_value is None:
                        total_filtered = self.count_total_clients()
                        query = "SELECT * FROM public.clients ORDER BY id LIMIT %s OFFSET %s"
                        cur.execute(query, (limit, offset))
                        data = cur.fetchall()
                    else:
                        count_query = "SELECT COUNT(*) FROM public.clients WHERE concat_ws(' ', name, phone_number, email) ILIKE %s"
                        cur.execute(count_query, (f"%{search_value}%",))
                        total_filtered = cur.fetchone()[0]

                        query = "SELECT * FROM public.clients WHERE concat_ws(' ', name, phone_number, email) ILIKE %s ORDER BY id LIMIT %s OFFSET %s"
                        cur.execute(
                            query,
                            (f"%{search_value}%", limit, offset),
                        )
                        data = cur.fetchall()

                    if not data:
                        return Response(success=False, error="No data found.")
                    else:
                        page = offset // limit + 1
                        clients = [
                            BaseClient(
                                id=client_data[0],
                                name=client_data[1],
                                phone_number=client_data[2],
                                email=client_data[3],
                                active=client_data[4],
                            )
                            for client_data in data
                        ]

                        return Response(
                            data=clients,
                            success=True,
                            metadata=Metadata(
                                total=total_filtered, page=page, size=limit
                            ),
                        )

        except psycopg2.Error as e:
            return Response(success=False, error=str(e))

    def delete_client(self, id: int):
        try:
            with self.connection.conn() as conn:
                with conn.cursor() as cur:
                    validation = self.find_client(id=id)
                    if not validation.success:
                        return Response(success=False)
                    else:

                        get_status_query = (
                            "SELECT active FROM public.clients WHERE id = %s"
                        )
                        cur.execute(get_status_query, (id,))
                        current_status = cur.fetchone()[0]

                        query = "UPDATE public.clients SET active = %s WHERE id = %s"
                        cur.execute(
                            query,
                            (
                                not current_status,
                                id,
                            ),
                        )
                        return Response(success=True)
        except Exception as e:
            return Response(success=False, error=str(e))

    def create_fake_clients(self):
        try:
            fake = Faker()
            fake.add_provider(E164Provider)

            with self.connection.conn() as conn:
                with conn.cursor() as cur:
                    for _ in range(40):
                        name = fake.name()
                        email = fake.email()
                        phone_number = fake.e164()

                        query = "INSERT INTO public.clients (name, phone_number, email, active) VALUES (%s, %s, %s, %s)"
                        cur.execute(query, (name, phone_number, email, True))
                        print("Creado con exito")

        except Exception as e:
            return Response(success=False, error=str(e))
