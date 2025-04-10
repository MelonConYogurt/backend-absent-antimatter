from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str
    phone_number: str


class UserUpdate(BaseModel):
    id: int
    name: str | None = None
    email: str | None = None
    phone_number: str | None = None


class UserSearch(BaseModel):
    search: str | None = None


class UserDelete(BaseModel):
    id: int
