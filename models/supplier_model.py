class Supplier:
    def __init__(
        self,
        name: str,
        phone: str,
        address: str,
        email: str,
        active: bool,
        id: int = None,
    ):
        self.name = name
        self.phone = phone
        self.address = address
        self.email = email
        self.active = active
        self.id = id
