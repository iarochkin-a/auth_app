from fastapi import APIRouter, Depends, Response, Request

from src.service.auth import AuthService
from src.schemas.token import RefreshTokenSchema, AccessTokenSchema, UserTokenSchema
from src.router.dependencies import get_auth_repository
from src.repository.auth import AuthRepository

auth_router = APIRouter(
    prefix='/token'
)


@auth_router.get('/get_tokens', response_model=UserTokenSchema)
async def get_users_token(
        request: Request):
    access_token = request.cookies.get('access_token')
    refresh_token = request.cookies.get('refresh_token')
    return UserTokenSchema(**{
        'access_token': access_token,
        'refresh_token': refresh_token
    })
