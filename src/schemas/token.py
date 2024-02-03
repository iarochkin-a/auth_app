from src.schemas import BaseSchema


class AccessTokenSchema(BaseSchema):
    access_token: str


class RefreshTokenSchema(BaseSchema):
    refresh_token: str


class UserTokenSchema(BaseSchema):
    access_token: str
    refresh_token: str
