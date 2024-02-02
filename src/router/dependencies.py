from src.repository.auth import AuthRepository
from src.config import Session


async def get_auth_repository() -> AuthRepository:
    session = Session()
    yield AuthRepository(session)
    await session.commit()
    await session.close()

