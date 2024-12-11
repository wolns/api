from src.models.base_model import BaseModel


class TokenPostResponseSchema(BaseModel):
    jwt_token: str


class TokenPostBodySchema(BaseModel):
    login: str
    password: str
