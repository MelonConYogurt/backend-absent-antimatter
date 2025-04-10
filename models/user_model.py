class UserBase:
    def __init__(self, name: str, email: str, phone_number: str):
        self.name = name
        self.email = email
        self.phone_number = phone_number


class UserResponse(UserBase):
    def __init__(
        self, name: str, email: str, phone_number: str, id: int, active: bool = True
    ):
        super().__init__(name, email, phone_number)
        self.id = id
        self.active = active


class UserUpdate:
    def __init__(
        self,
        id: int,
        name: str | None = None,
        email: str | None = None,
        phone_number: str | None = None,
    ):
        self.id = id
        self.name = name
        self.email = email
        self.phone_number = phone_number


class UserSearch:
    def __init__(
        self,
        search: str | None = None,
    ):
        self.search = search


class UserDelete:
    def __init__(self, id: int):
        self.id = id
