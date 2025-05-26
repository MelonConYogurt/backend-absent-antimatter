class Sale:
    def __init__(self, client_id: int, user_id: int, total: int, price: int):
        self.client_id = client_id
        self.user_id = user_id
        self.total = total
        self.price = price
