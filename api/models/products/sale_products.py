from pydantic import BaseModel


class SaleProduct(BaseModel):
    id: int
    quantity: int
    price: float


class Sale(BaseModel):
    client_id: int
    user_id: int
    total: float
