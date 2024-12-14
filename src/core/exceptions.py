from fastapi import HTTPException


class TokenExpiredException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Token expired")
