from database.conection import Connection
from models.response_model import Response, Metadata
from faker import Faker


class Crud:
    def __init__(self):
        self.conection = Connection()

    def validate_categorie(self, name: str):
        try:
            with self.conection.conn() as conn:
                with conn.cursor() as cur:
                    query = "SELECT * FROM public.categories WHERE name = %s"
                    cur.execute(query, (name,))
                    response = cur.fetchone()
                    if response is None:
                        return Response(success=True)
                    else:
                        return Response(success=False)
        except Exception as e:
            print(e)

    def create_categorie(self, name: str):
        try:
            validation = self.validate_categorie(name=name)
            if not validation.success:
                return Response(
                    success=False, error=f"Already one category like this : {name}"
                )
            else:
                with self.conection.conn() as conn:
                    with conn.cursor() as cur:
                        query = "INSERT INTO public.categories (name) VALUES (%s) RETURNING id"
                        cur.execute(query, (name,))
                        response = cur.fetchone()[0]
                        if not response:
                            return Response(success=False)
                        else:
                            return Response(success=True)

        except Exception as e:
            print(e)

    def create_fake_categories(self):
        try:
            fake = Faker()

            for _ in range(10):
                category_name = fake.word().capitalize()
                self.create_categorie(name=category_name)

            return Response(
                success=True,
            )
        except Exception as e:
            print(e)
            return Response(success=False, error=str(e))
