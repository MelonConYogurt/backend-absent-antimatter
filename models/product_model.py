from datetime import datetime


class Product:
    def __init__(
        self,
        id: int,
        name: str,
        stock: int,
        reference: str,
        category_id: int,
        price: float,
        created_at: datetime,
        supplier_id: int,
        active: bool,
    ):
        self.id = id
        self.name = name
        self.stock = stock
        self.reference = reference
        self.category_id = category_id
        self.price = price
        self.created_at = created_at
        self.supplier_id = supplier_id
        self.active = active


class ProductBasic:
    def __init__(
        self,
        id: int,
        name: str,
        stock: int,
        reference: str,
        category_id: int,
        price: float,
        supplier_id: int,
    ):
        self.id = id
        self.name = name
        self.stock = stock
        self.reference = reference
        self.category_id = category_id
        self.price = price
        self.supplier_id = supplier_id
