from src.schemas import BaseSchema


class InputUserSchema(BaseSchema):
    username: str
    password_hash: str
    email: str
    role_id: int = 1


class OutputUserSchema(InputUserSchema):
    id: int


class InputRoleSchema(BaseSchema):
    title: str


class OutputRoleSchema(InputRoleSchema):
    id: int


class RegisterUserSchema(BaseSchema):
    username: str
    email: str
    password: str
    repeated_password: str


class SingInUserSchema(BaseSchema):
    username: str
    password: str
