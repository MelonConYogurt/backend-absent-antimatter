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

    def search_client(
        self,
        limit: int,
        offset: int,
        search_value: str | None = None,
        order_direction: str | None = "ASC",
        column: str | None = "id",
    ):

        VALID_COLS = {"id", "name", "phone_number", "email", "active"}
        VALID_ORDERS = {"ASC", "DESC"}

        order_direction = order_direction if order_direction in VALID_ORDERS else "id"
        column = column if column in VALID_COLS else "ASC"

        order_clause = f"ORDER BY {column} {order_direction}"
        like_pattren = f"%{search_value or ''}%"

        try:
            with self.connection.conn() as conn:
                with conn.cursor() as cur:

                    query = f"""
                    SELECT *
                    FROM public.clients
                    WHERE name ILIKE  %s OR phone_number ILIKE  %s  OR email ILIKE %s
                    {order_clause}
                    LIMIT %s OFFSET %s
                    """
                    cur.execute(
                        query,
                        (
                            like_pattren,
                            like_pattren,
                            like_pattren,
                            limit,
                            offset,
                        ),
                    )
                    data = cur.fetchall()

                    total = """
                        SELECT COUNT(*) 
                        FROM public.clients 
                        WHERE name ILIKE %s OR phone_number ILIKE %s OR email ILIKE %s
                        """
                    cur.execute(
                        total,
                        (like_pattren, like_pattren, like_pattren),
                    )
                    total = cur.fetchone()[0]

                    if not data:
                        return Response(success=False, error="No data found.")
                    else:
                        page = offset // limit + 1
                        return Response(
                            data=[
                                BaseClient(
                                    id=client_data[0],
                                    name=client_data[1],
                                    phone_number=client_data[2],
                                    email=client_data[3],
                                    active=client_data[4],
                                )
                                for client_data in data
                            ],
                            success=True,
                            metadata=Metadata(total=total, page=page, size=limit),
                        )
        except psycopg2.Error as e:
            return Response(success=False, error=str(e))

    def delete_client(self, id: int):
        try:
            with self.connection.conn() as conn:
                with conn.cursor() as cur:
                    validation = self.find_client(id=id)
                    if not validation.success:
                        return Response(success=False, error="Cliente no encontrado")

                    query = "DELETE FROM public.clients WHERE id = %s RETURNING id"
                    cur.execute(query, (id,))
                    response = cur.fetchone()
                    if not response:
                        return Response(
                            success=False, error="No se pudo eliminar el cliente"
                        )
                    else:
                        return Response(
                            success=True, data={"deleted_client_id": response[0]}
                        )
        except Exception as e:
            return Response(success=False, error=str(e))

    def toggle_active_state(self, id: int):
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

                        query = "UPDATE public.clients SET active = %s WHERE id = %s RETURNING id"
                        cur.execute(
                            query,
                            (
                                not current_status,
                                id,
                            ),
                        )
                        response = cur.fetchone()
                        return Response(
                            success=True, data={"toggled_client_id": response[0]}
                        )
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
