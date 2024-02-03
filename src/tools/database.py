from src.schemas.auth import RegisterUserSchema, InputUserSchema, OutputUserSchema
from src.tools.hasher import Hasher


class Database_tools:

    @staticmethod
    async def convert_register_schema(user_register_schema: RegisterUserSchema) -> InputUserSchema:
        user_register_dict = user_register_schema.__dict__
        user_register_dict['password_hash'] = Hasher.get_password_hash(user_register_schema.password)
        user_register_dict.pop('password')
        user_register_dict.pop('repeated_password')
        return InputUserSchema(**user_register_dict)

    @staticmethod
    async def convert_output_schema(user_output_schema: OutputUserSchema) -> InputUserSchema:
        user_output_dict = user_output_schema.__dict__
        user_output_dict.pop('id')
        return InputUserSchema(**user_output_dict)
