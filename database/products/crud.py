from database.conection import Connection
from models.response_model import Response, Metadata


class Crud:
    def __init__(self):
        self.conection = Connection.conn()
