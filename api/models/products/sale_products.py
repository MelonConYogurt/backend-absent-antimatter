from pydantic import BaseModel


class SaleProduct(BaseModel):
    id: int
    quantity: int
    price: float
