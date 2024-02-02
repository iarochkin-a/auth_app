from sqlalchemy.exc import NoResultFound, IntegrityError
from fastapi import HTTPException
from src.repository.interfaces.auth import AuthRepositoryInterface
from src.schemas.auth import InputUserSchema, OutputUserSchema


class AuthService:

    def __init__(self, auth_repository: AuthRepositoryInterface):
        self.auth_repository = auth_repository

    async def set_user(self, user_schema: InputUserSchema):
        try:
            await self.auth_repository.set_obj(user_schema)
        except IntegrityError as ex:
            if 'username' in ex.args[0]:
                ex.detail = f'User with username: {user_schema.username} already exist.'
            elif 'email' in ex.args[0]:
                ex.detail = f'User with email: {user_schema.email} already exist.'
            elif 'role_id' in ex.args[0]:
                ex.detail = f'Incorrect role id: {user_schema.role_id}.'
            raise HTTPException(
                status_code=400,
                detail=f'{ex.detail}'
            )
        except Exception:
            raise HTTPException(
                status_code=500,
                detail=f'Database error'
            )

    async def get_user(self, user_id: int) -> OutputUserSchema:
        try:
            racks_schema: OutputUserSchema = await self.auth_repository.get_obj(user_id)
            return racks_schema
        except NoResultFound:
            raise HTTPException(
                status_code=400,
                detail=f'User with id {user_id} not found.'
            )
        except Exception:
            raise HTTPException(
                status_code=500,
                detail=f'Database error'
            )

    async def get_all__users(self) -> list[OutputUserSchema]:
        try:
            racks_schemas_list: [OutputUserSchema] = await self.auth_repository.get_all_obj()
            return racks_schemas_list
        except Exception:
            raise HTTPException(
                status_code=500,
                detail=f'Database error'
            )

    async def update_user(self, user_id: int, user_schema: InputUserSchema):
        try:
            await self.auth_repository.update_obj(user_id, user_schema)
        except NoResultFound:
            raise HTTPException(
                status_code=400,
                detail=f'User with id {user_id} not found.'
            )
        except IntegrityError as ex:
            if 'username' in ex.args[0]:
                ex.detail = f'User with username {user_schema.username} already exist.'
            elif 'email' in ex.args[0]:
                ex.detail = f'User with email {user_schema.email} already exist.'
            elif 'role_id' in ex.args[0]:
                ex.detail = f'Incorrect role id: {user_schema.role_id}.'
            raise HTTPException(
                status_code=400,
                detail=f'{ex.detail}'
            )
        except Exception:
            raise HTTPException(
                status_code=500,
                detail=f'Database error'
            )

    async def delete_user(self, user_id: int):
        try:
            await self.auth_repository.delete_obj(user_id)
        except NoResultFound:
            raise HTTPException(
                status_code=400,
                detail=f'User with id {user_id} not found.'
            )
        except Exception:
            raise HTTPException(
                status_code=500,
                detail=f'Database error'
            )
