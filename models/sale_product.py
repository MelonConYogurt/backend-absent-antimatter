class SaleProduct:
    def __init__(self, id: int, quantity: float, sale_id: int):
        self.id = id
        self.quantity = quantity
        self.sale_id = sale_id


class Product:
    def __init__(self, id: int, quantity: float, price: float):
        self.id = id
        self.quantity = quantity
        self.price = price
