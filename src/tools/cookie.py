from fastapi import Request, Response
from src.schemas.token import UserTokenSchema


class Cookie_tools:

    @staticmethod
    async def get_user_token(request: Request):
        access_token = request.cookies.get('access_token')
        refresh_token = request.cookies.get('refresh_token')
        return UserTokenSchema(**{
            "access_token": access_token,
            "refresh_token": refresh_token
        })

    @staticmethod
    async def set_user_token(response: Response, user_token_schema: UserTokenSchema):
        response.set_cookie('access_token', user_token_schema.access_token)
        response.set_cookie('refresh_token', user_token_schema.refresh_token)
