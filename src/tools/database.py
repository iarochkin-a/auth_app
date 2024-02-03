from src.schemas.auth import RegisterUserSchema, InputUserSchema, OutputUserSchema, PatchUserSchema
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

    @staticmethod
    async def convert_patch_user_schema(patch_user_schema: PatchUserSchema, main_user_schema: OutputUserSchema) -> InputUserSchema:
        result_user_dict = dict()
        for i in patch_user_schema.__dict__:
            if patch_user_schema.__dict__[i] is not None:
                result_user_dict[i] = patch_user_schema.__dict__[i]
            else:
                result_user_dict[i] = main_user_schema.__dict__[i]
        return InputUserSchema(**result_user_dict)
