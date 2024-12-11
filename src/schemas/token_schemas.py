from src.models.base_model import BaseModel


class TokenPostResponseSchema(BaseModel):
    access_token: str


class TokenPostBodySchema(BaseModel):
    login: str
    password: str
