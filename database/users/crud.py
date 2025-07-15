from database.connection import Connection
from models.user_model import User
from models.response_model import Response, Metadata
from faker import Faker
from faker_e164.providers import E164Provider
import psycopg2


class Crud:
    def __init__(self):
        self.Connection = Connection()

    def find_user_by_id(self, id: int):
        try:
            query = "SELECT * FROM PUBLIC.users WHERE id = %s"
            with self.Connection.conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (id,))
                    data = cur.fetchone()
                    if data:
                        return Response(data=data, success=True)
                    else:
                        return Response(success=False)
        except psycopg2.Error as e:
            return Response(success=False, error=str(e))

    def find_user_by_email(self, email: str):
        try:
            query = "SELECT * FROM PUBLIC.users WHERE email = %s"
            with self.Connection.conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (email,))
                    data = cur.fetchone()
                    if data:
                        return Response(data=data, success=True)
                    else:
                        return Response(success=False)
        except psycopg2.Error as e:
            return Response(success=False, error=str(e))

    def create_user(self, data: User):
        try:
            user_exist = self.find_user_by_email(data.email)
            if not user_exist.data:
                with self.Connection.conn() as conn:
                    with conn.cursor() as cur:
                        query = "INSERT INTO public.users (name, email, phone_number, role) VALUES(%s, %s, %s, %s)"
                        cur.execute(
                            query, (data.name, data.email, data.phone_number, data.role)
                        )
                        return Response(data=data, success=True)
            return Response(success=False, error="Usuario ya existe")
        except psycopg2.Error as e:
            return Response(success=False, error=str(e))

    def update_user(self, data: User):
        try:
            user_exist = self.find_user_by_id(data.id)
            if not user_exist.success:
                return Response(
                    success=False,
                    error="Usuario no encontrado",
                )

            with self.Connection.conn() as conn:
                with conn.cursor() as cur:
                    query = "UPDATE public.users set name=%s, phone_number=%s, email=%s, role=%s WHERE id =%s"
                    cur.execute(
                        query,
                        (
                            data.name,
                            data.phone_number,
                            data.email,
                            data.role,
                            data.id,
                        ),
                    )
                    return Response(
                        success=True, data="Usuario actualizado exitosamente"
                    )

        except psycopg2.Error as e:
            return Response(success=False, error=str(e))

    def delete_user(self, user_id: int):
        try:
            user_exist = self.find_user_by_id(user_id)
            if user_exist.data:
                with self.Connection.conn() as conn:
                    with conn.cursor() as cur:
                        query = "DELETE FROM public.users WHERE id=%s"
                        cur.execute(query, (user_id,))
                        return Response(
                            success=True, data="Usuario eliminado exitosamente"
                        )
            return Response(success=False, error="Usuario no encontrado")
        except psycopg2.Error as e:
            return Response(success=False, error=str(e))

    def search_user(
        self,
        offset: int,
        limit: int,
        order_direction: str | None = "ASC",
        search_value: str | None = None,
        column: str | None = "id",
    ):

        VALID_COLS = {"id", "name", "phone_number", "email", "role", "active"}
        VALID_ORDERS = {"ASC", "DESC"}

        column = column if column in VALID_COLS else "id"
        order_direction = order_direction if order_direction in VALID_ORDERS else "ASC"

        try:
            with self.Connection.conn() as conn:
                with conn.cursor() as cur:

                    order_clause = f"ORDER BY {column} {order_direction}"
                    like_pattern = f"%{search_value or ''}%"

                    total = """
                    SELECT COUNT(*) FROM public.users 
                    WHERE name ILIKE %s OR email ILIKE %s OR phone_number ILIKE %s OR id::text ILIKE %s
                    """
                    cur.execute(
                        total,
                        (
                            like_pattern,
                            like_pattern,
                            like_pattern,
                            like_pattern,
                        ),
                    )
                    total = cur.fetchone()[0]

                    query = f"""
                    SELECT * FROM public.users 
                    WHERE name ILIKE %s OR email ILIKE %s OR phone_number ILIKE %s OR id::text ILIKE %s 
                    {order_clause} 
                    LIMIT %s OFFSET %s
                    """

                    cur.execute(
                        query,
                        (
                            like_pattern,
                            like_pattern,
                            like_pattern,
                            like_pattern,
                            limit,
                            offset,
                        ),
                    )
                    users = cur.fetchall()
                    page = offset // limit + 1

                    return Response(
                        success=True,
                        data=[
                            User(
                                id=int(user[0]),
                                name=user[1],
                                phone_number=user[2],
                                email=user[3],
                                active=bool(user[4]),
                                role=user[5],
                            )
                            for user in users
                        ],
                        metadata=Metadata(page=page, size=limit, total=total),
                    )
        except psycopg2.Error as e:
            return Response(success=False, error=str(e))

    def change_user_active_state(self, data: User):
        try:
            user_exist = self.find_user_by_id(id=data.id)
            if not user_exist.success:
                return Response(success=False)
            else:
                with self.Connection.conn() as conn:
                    with conn.cursor() as cur:
                        query = "UPDATE public.users set active = %s WHERE id = %s "
                        cur.execute(query, (not data.active, data.id))
                        return Response(
                            data=User(
                                id=data.id,
                                name=user_exist.data[1],
                                phone_number=user_exist.data[2],
                                email=user_exist.data[3],
                                active=not data.active,
                                role=(
                                    user_exist.data[5]
                                    if len(user_exist.data) > 5
                                    else "user"
                                ),
                            ),
                            success=True,
                        )

        except psycopg2.Error as e:
            return Response(success=False, error=str(e))

    def create_fake_users(self):
        try:
            fake = Faker()
            fake.add_provider(E164Provider)

            with self.Connection.conn() as conn:
                with conn.cursor() as cur:
                    for _ in range(40):
                        name = fake.name()
                        email = fake.email()
                        phone_number = fake.e164()
                        role = fake.job()

                        query = "INSERT INTO public.users (name, phone_number, email, active, role) VALUES (%s, %s, %s, %s, %s)"
                        cur.execute(query, (name, phone_number, email, True, role))
                        print("Creado con exito")

        except Exception as e:
            return Response(success=False, error=str(e))
