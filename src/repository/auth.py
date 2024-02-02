from src.repository import BaseSQLRepository
from src.repository.interfaces.auth import AuthRepositoryInterface
from src.models.auth import UserORM
from src.schemas.auth import OutputUserSchema


class AuthRepository(BaseSQLRepository, AuthRepositoryInterface):
    model = UserORM
    schema = OutputUserSchema
