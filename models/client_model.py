class BaseClient:
    def __init__(self, id: str, name: str, phone_number: str, email: str, active: bool):
        self.id = id
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.active = active
