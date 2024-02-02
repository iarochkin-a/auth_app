from src.schemas import BaseSchema


class InputUserSchema(BaseSchema):
    username: str
    password_hash: str
    email: str
    role_id: int


class OutputUserSchema(InputUserSchema):
    id: int


class InputRoleSchema(BaseSchema):
    title: str


class OutputRoleSchema(InputRoleSchema):
    id: int
