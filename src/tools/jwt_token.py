from datetime import datetime, timedelta

import jwt

from src.config import JWT_settings
from src.schemas.auth import InputUserSchema
from src.schemas.token import AccessTokenSchema, RefreshTokenSchema, UserTokenSchema


class JWT_tools:

    @staticmethod
    async def get_access_token(user_schema: InputUserSchema) -> AccessTokenSchema:
        user_schema_dict = user_schema.__dict__
        user_schema_dict.pop('password_hash')
        user_schema_dict.pop('refresh_token')

        decoded_dict = {
            'iss': JWT_settings().ISS,
            'sub': JWT_settings().SUB,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(seconds=JWT_settings().ACCESS_TOKEN_EXP_TIME),
            'payload': user_schema_dict
        }
        access_token = jwt.encode(decoded_dict, JWT_settings().SECRET_KEY, JWT_settings().ALGORITHM)
        return AccessTokenSchema(**{'access_token': access_token})

    @staticmethod
    async def get_refresh_token(user_schema: InputUserSchema) -> RefreshTokenSchema:
        user_schema_dict = user_schema.__dict__
        print(user_schema)
        user_schema_dict.pop('password_hash')
        user_schema_dict.pop('refresh_token')

        decoded_dict = {
            'iss': JWT_settings().ISS,
            'sub': JWT_settings().SUB,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(seconds=JWT_settings().REFRESH_TOKEN_EXP_TIME),
            'payload': user_schema_dict
        }
        refresh_token = jwt.encode(decoded_dict, JWT_settings().SECRET_KEY, JWT_settings().ALGORITHM)
        return RefreshTokenSchema(**{'refresh_token': refresh_token})

    @classmethod
    async def get_user_tokens(cls, user_schema: InputUserSchema) -> UserTokenSchema:
        access_token: AccessTokenSchema = await cls.get_access_token(user_schema.copy())
        refresh_token: RefreshTokenSchema = await cls.get_refresh_token(user_schema)
        return UserTokenSchema(**{
            'access_token': access_token.access_token,
            'refresh_token': refresh_token.refresh_token
        })
