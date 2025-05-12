from pydantic import BaseModel


class User(BaseModel):
    id: int | None = None
    name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    active: bool = True
    role: str = "user"
