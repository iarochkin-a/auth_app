from src.repository import BaseSQLRepository
from src.repository.interfaces.auth import AuthRepositoryInterface
from src.models.auth import UserORM
from src.schemas.auth import OutputUserSchema, InputUserSchema

from sqlalchemy import select


class AuthRepository(BaseSQLRepository, AuthRepositoryInterface):
    model = UserORM
    schema = OutputUserSchema

    async def get_user_by_username(self, username: str) -> OutputUserSchema:
        query = (select(self.model)
                 .where(self.model.username == username)
                 )
        user_row = await self.session.execute(query)
        if not user_row:
            raise Exception(f'{self.model.__name__} with id {self.model.id} not found.')
        user_model = user_row.scalar_one()
        return self.schema.model_validate(user_model)
