from fastapi import APIRouter, Depends

from src.service.auth import AuthService
from src.schemas.auth import OutputUserSchema, InputUserSchema
from src.router.dependencies import get_auth_repository
from src.repository.auth import AuthRepository

auth_router = APIRouter(
    prefix='/auth'
)


@auth_router.get('/get_user', response_model=OutputUserSchema)
async def get_user(
        user_id: int,
        auth_repository=Depends(get_auth_repository)):
    rack_schema = await AuthService(auth_repository).get_user(user_id)
    return rack_schema


@auth_router.get('/get_all_users', response_model=list[OutputUserSchema])
async def get_all_users(
        auth_repository=Depends(get_auth_repository)):
    rack_schemas_list = await AuthService(auth_repository).get_all__users()
    return rack_schemas_list


@auth_router.post('/set_user')
async def set_user(user_schema: InputUserSchema,
                   auth_repository=Depends(get_auth_repository)):
    await AuthService(auth_repository).set_user(user_schema)


@auth_router.put('/update_user')
async def update_user(user_id: int,
                      user_schema: InputUserSchema,
                      auth_repository=Depends(get_auth_repository)
                      ):
    await AuthService(auth_repository).update_user(user_id, user_schema)


@auth_router.delete('/delete_user')
async def delete_user(user_id: int,
                      auth_repository=Depends(get_auth_repository)):
    await AuthService(auth_repository).delete_user(user_id)
