from src.schemas import BaseSchema


class InputUserSchema(BaseSchema):
    username: str
    password_hash: str
    email: str
    role_id: int = 1
    refresh_token: str = None


class OutputUserSchema(InputUserSchema):
    id: int


class InputRoleSchema(BaseSchema):
    title: str


class OutputRoleSchema(InputRoleSchema):
    id: int


class PatchUserSchema(BaseSchema):
    username: str | None = None
    password_hash: str | None = None
    email: str | None = None
    role_id: int | None = 1
    refresh_token: str | None = None


class RegisterUserSchema(BaseSchema):
    username: str
    email: str
    password: str
    repeated_password: str


class SingInUserSchema(BaseSchema):
    username: str
    password: str
