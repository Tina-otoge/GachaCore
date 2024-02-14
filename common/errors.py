from fastapi import HTTPException


class NotFound(HTTPException):
    def __init__(self, table, search):
        super().__init__(
            status_code=404, detail=f"{table.__name__} not found: {search}"
        )
