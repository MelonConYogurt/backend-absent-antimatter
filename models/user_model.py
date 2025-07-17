class User:
    def __init__(
        self,
        name: str = None,
        email: str = None,
        phone_number: str = None,
        id: int = None,
        active: bool = True,
        role: str = "user",
    ):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.id = id
        self.active = active
        self.role = role


class UserAuthentication:
    def __init__(
        self,
        hashed_password: str,
        name: str = None,
        email: str = None,
        phone_number: str = None,
        id: int = None,
        disabled: bool = True,
        role: str = "user",
    ):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.id = id
        self.disabled = disabled
        self.role = role
        self.hashed_password = hashed_password
