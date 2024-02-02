from passlib.context import CryptContext

pwb_context = CryptContext(schemes=["bcrypt"])


class Hasher:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwb_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwb_context.hash(password)
