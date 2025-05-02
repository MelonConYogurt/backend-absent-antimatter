from pydantic import BaseModel


class ClientBase(BaseModel):
    id: int
    name: str
    email: str
    phone_number: str
