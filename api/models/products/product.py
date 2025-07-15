from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    stock: int
    reference: str
    category_id: int
    price: float
    supplier_id: int

