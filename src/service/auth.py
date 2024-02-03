from sqlalchemy.exc import NoResultFound, IntegrityError
from fastapi import HTTPException
from src.repository.interfaces.auth import AuthRepositoryInterface
from src.schemas.auth import InputUserSchema, OutputUserSchema, RegisterUserSchema, SingInUserSchema, PatchUserSchema
from src.schemas.token import UserTokenSchema
from src.tools.database import Database_tools
from src.tools.hasher import Hasher
from src.tools.jwt_token import JWT_tools


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

    async def update_part_of_user_model(self, user_id: int, patch_user_schema: PatchUserSchema):
        try:
            main_user_schema = await self.get_user(user_id)
            new_user_schema: InputUserSchema = await Database_tools.convert_patch_user_schema(patch_user_schema, main_user_schema)
            print(new_user_schema.__dict__)
            await self.auth_repository.update_obj(user_id, new_user_schema)
        except NoResultFound:
            raise HTTPException(
                status_code=400,
                detail=f'User with id {user_id} not found.'
            )
        except IntegrityError as ex:
            if 'username' in ex.args[0]:
                ex.detail = f'User with username {patch_user_schema.username} already exist.'
            elif 'email' in ex.args[0]:
                ex.detail = f'User with email {patch_user_schema.email} already exist.'
            elif 'role_id' in ex.args[0]:
                ex.detail = f'Incorrect role id: {patch_user_schema.role_id}.'
            raise HTTPException(
                status_code=400,
                detail=f'{ex.detail}'
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

    async def create_new_user(self, register_user_schema: RegisterUserSchema):
        try:
            if register_user_schema.password != register_user_schema.repeated_password:
                raise ValueError
            user_schema: InputUserSchema = await Database_tools.convert_register_schema(register_user_schema)
            user_token_schema: UserTokenSchema = await JWT_tools.get_user_tokens(user_schema.copy())
            user_schema.refresh_token = user_token_schema.refresh_token
            await self.auth_repository.set_obj(user_schema)
            return user_token_schema
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f'The passwords are not same.'
            )
        except IntegrityError as ex:
            if 'username' in ex.args[0]:
                ex.detail = f'User with username: {register_user_schema.username} already exist.'
            elif 'email' in ex.args[0]:
                ex.detail = f'User with email: {register_user_schema.email} already exist.'
            elif 'role_id' in ex.args[0]:
                ex.detail = f'Incorrect role id: {register_user_schema.role_id}.'
            raise HTTPException(
                status_code=400,
                detail=f'{ex.detail}'
            )
        except Exception:
            raise HTTPException(
                status_code=500,
                detail=f'Database error'
            )

    async def verify_user(self, sing_in_user_schema: SingInUserSchema):
        try:
            user_output_schema: OutputUserSchema = await self.auth_repository.get_user_by_username(sing_in_user_schema.username)
            if not Hasher.verify_password(sing_in_user_schema.password, user_output_schema.password_hash):
                raise ValueError
            user_schema: InputUserSchema = await Database_tools.convert_output_schema(user_output_schema)
            user_token_schema: UserTokenSchema = await JWT_tools.get_user_tokens(user_schema.copy())
            user_schema.refresh_token = user_token_schema.refresh_token
            return user_token_schema

        except ValueError:
            raise HTTPException(
                status_code=402,
                detail=f'Incorrect password.'
            )
        except NoResultFound:
            raise HTTPException(
                status_code=400,
                detail=f'User with username {sing_in_user_schema.username} not found.'
            )
        except Exception:
            raise HTTPException(
                status_code=500,
                detail=f'Database error'
            )
