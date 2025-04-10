from typing import Any


class Metadata:
    def __init__(
        self,
        page: int | None = None,
        size: int | None = None,
        total: int | None = None,
    ):
        self.page = page
        self.size = size
        self.total = total


class Response:
    def __init__(
        self,
        data: Any | None = None,
        success: bool | None = None,
        error: str | None = None,
        metadata: Metadata | None = None,
    ):
        self.metadata = metadata
        self.data = data
        self.success = success
        self.error = error
