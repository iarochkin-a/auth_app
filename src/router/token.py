from fastapi import APIRouter, Depends, Response, Request

from src.service.auth import AuthService
from src.schemas.token import RefreshTokenSchema, AccessTokenSchema, UserTokenSchema
from src.router.dependencies import get_auth_repository
from src.repository.auth import AuthRepository

token_router = APIRouter(
    prefix='/token'
)


@token_router.get('/get_tokens', response_model=UserTokenSchema)
async def get_users_token(
        request: Request):
    access_token = request.cookies.get('access_token')
    refresh_token = request.cookies.get('refresh_token')
    return UserTokenSchema(**{
        'access_token': access_token,
        'refresh_token': refresh_token
    })
    
    
@token_router.get('/verify_tokens')
async def verify_user_tokens(
        request: Request,
        auth_repository: AuthRepository = Depends(get_auth_repository)):
    access_token = request.cookies.get('access_token')
    refresh_token = request.cookies.get('refresh_token')
    await AuthService(auth_repository).verify_tokens(UserTokenSchema(**{
        'access_token': access_token,
        'refresh_token': refresh_token
    }))
