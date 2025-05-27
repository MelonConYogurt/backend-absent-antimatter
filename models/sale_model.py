from datetime import datetime


class Sale:
    def __init__(
        self,
        client_id: int,
        user_id: int,
        total: float,
        id: int | None = None,
        sale_date: datetime | None = None,
    ):
        self.client_id = client_id
        self.user_id = user_id
        self.total = total
        self.id = id
        self.sale_date = sale_date
