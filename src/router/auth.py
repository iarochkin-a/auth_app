from fastapi import APIRouter, Depends, Request, Response

from src.service.auth import AuthService
from src.schemas.auth import OutputUserSchema, InputUserSchema, RegisterUserSchema, SingInUserSchema, PatchUserSchema
from src.schemas.token import UserTokenSchema
from src.router.dependencies import get_auth_repository
from src.repository.auth import AuthRepository
from src.tools.cookie import Cookie_tools

auth_router = APIRouter(
    prefix='/auth'
)


@auth_router.get('/get_user', response_model=OutputUserSchema)
async def get_user(
        user_id: int,
        auth_repository: AuthRepository = Depends(get_auth_repository)):
    rack_schema = await AuthService(auth_repository).get_user(user_id)
    return rack_schema


@auth_router.get('/get_all_users', response_model=list[OutputUserSchema])
async def get_all_users(
        auth_repository: AuthRepository = Depends(get_auth_repository)):
    rack_schemas_list = await AuthService(auth_repository).get_all__users()
    return rack_schemas_list


@auth_router.post('/set_user')
async def set_user(user_schema: InputUserSchema,
                   auth_repository: AuthRepository = Depends(get_auth_repository)):
    await AuthService(auth_repository).set_user(user_schema)


@auth_router.patch('/patch_user')
async def patch_user(user_id: int,
                     user_schema: PatchUserSchema,
                     auth_repository: AuthRepository = Depends(get_auth_repository)):
    await AuthService(auth_repository).update_part_of_user_model(user_id, user_schema)
    return user_schema


@auth_router.put('/update_user')
async def update_user(user_id: int,
                      user_schema: InputUserSchema,
                      auth_repository: AuthRepository = Depends(get_auth_repository)
                      ):
    await AuthService(auth_repository).update_user(user_id, user_schema)


@auth_router.delete('/delete_user')
async def delete_user_from_db(user_id: int,
                              auth_repository: AuthRepository = Depends(get_auth_repository)):
    await AuthService(auth_repository).delete_user(user_id)


@auth_router.post('/register')
async def register_new_user(register_user_schema: RegisterUserSchema,
                            response: Response,
                            auth_repository: AuthRepository = Depends(get_auth_repository)):
    user_tokens: UserTokenSchema = await AuthService(auth_repository).create_new_user(register_user_schema)
    await Cookie_tools.set_user_token(response, user_tokens)


@auth_router.post('/sing_in')
async def authorize_user(sing_in_user_schema: SingInUserSchema,
                         response: Response,
                         auth_repository: AuthRepository = Depends(get_auth_repository)):
    user_tokens: UserTokenSchema = await AuthService(auth_repository).verify_user(sing_in_user_schema)
    await Cookie_tools.set_user_token(response, user_tokens)
