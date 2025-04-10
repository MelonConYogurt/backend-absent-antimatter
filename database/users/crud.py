from database.conection import Connection
from models.user_model import (
    UserBase,
    UserResponse,
    UserUpdate,
    UserSearch,
    UserDelete,
)
from models.response_model import Response, Metadata
import psycopg2


class Crud:
    def __init__(self):
        self.Connection = Connection()

    def count_total_users(self):
        try:
            with self.Connection.conn() as conn:
                with conn.cursor() as cur:
                    query = "SELECT COUNT(*) FROM public.users"
                    cur.execute(query)
                    total = cur.fetchone()[0]
                    return total
        except psycopg2.Error as e:
            return 0

    def list_user(self, offset: int, limit: int):
        try:
            with self.Connection.conn() as conn:
                with conn.cursor() as cur:
                    query = "SELECT * FROM public.users OFFSET %s LIMIT %s"
                    cur.execute(query, (offset, limit))
                    users_data = cur.fetchall()
                    total_users = self.count_total_users()
                    if users_data:
                        users = [
                            UserResponse(
                                id=int(user_data[0]),
                                name=user_data[1],
                                phone_number=user_data[2],
                                email=user_data[3],
                                active=bool(user_data[4]),
                            )
                            for user_data in users_data
                        ]
                        page = offset / limit
                        return Response(
                            data=users,
                            success=True,
                            metadata=Metadata(page=page, size=limit, total=total_users),
                        )
                    else:
                        return Response(
                            success=True,
                            data=[],
                            metadata=Metadata(page=0, size=limit, total=total_users),
                        )
        except psycopg2.Error as e:
            return Response(error=str(e), success=False)

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

    def create_user(self, data: UserBase):
        try:
            user_exist = self.find_user_by_email(data.email)
            if not user_exist.data:
                with self.Connection.conn() as conn:
                    with conn.cursor() as cur:
                        query = "INSERT INTO public.users (name, email, phone_number) VALUES(%s, %s, %s)"
                        cur.execute(query, (data.name, data.email, data.phone_number))
                        return Response(data=data, success=True)
            return Response(success=False, error="Usuario ya existe")
        except psycopg2.Error as e:
            return Response(success=False, error=str(e))

    def update_user(self, data: UserUpdate):
        try:
            user_exist = self.find_user_by_id(data.id)
            new_user_exist = self.find_user_by_email(data.email)
            if not user_exist.success:
                return Response(
                    success=False,
                    error="Usuario no encontrado",
                )
            elif not new_user_exist.success:
                with self.Connection.conn() as conn:
                    with conn.cursor() as cur:
                        query = "UPDATE public.users set name=%s, phone_number=%s, email=%s WHERE id =%s"
                        cur.execute(
                            query,
                            (
                                data.name,
                                data.phone_number,
                                data.email,
                                data.id,
                            ),
                        )
                        return Response(
                            success=True, data="Usuario actualizado exitosamente"
                        )
            else:
                return Response(
                    success=False,
                    error="Usuario con email repetido, el nuevo email ya existe",
                )
        except psycopg2.Error as e:
            return Response(success=False, error=str(e))

    def delete_user(self, data: UserDelete):
        try:
            user_exist = self.find_user_by_id(data.id)
            if user_exist.data:
                with self.Connection.conn() as conn:
                    with conn.cursor() as cur:
                        query = "DELETE FROM public.users WHERE id=%s"
                        cur.execute(query, (data.id,))
                        return Response(
                            success=True, data="Usuario eliminado exitosamente"
                        )
            return Response(success=False, error="Usuario no encontrado")
        except psycopg2.Error as e:
            return Response(success=False, error=str(e))

    def search_user(self, data: UserSearch, offset: int, limit: int):
        try:
            query = "SELECT * FROM public.users WHERE name ILIKE %s OR email ILIKE %s OR phone_number ILIKE %s LIMIT %s OFFSET %s"
            search_pattern = f"%{data.search}%"
            with self.Connection.conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        query,
                        (search_pattern, search_pattern, search_pattern, limit, offset),
                    )
                    result_data = cur.fetchall()
                    if result_data:
                        users = [
                            UserResponse(
                                id=int(element[0]),
                                name=element[1],
                                phone_number=element[2],
                                email=element[3],
                                active=bool(element[4]),
                            )
                            for element in result_data
                        ]
                        return Response(success=True, data=users)
                    return Response(success=False, error="No se encontraron usuarios")
        except psycopg2.Error as e:
            return Response(success=False, error=str(e))
