from src.router.auth import auth_router
from src.router.token import token_router
from fastapi import APIRouter


def get_router() -> [APIRouter]:
    return [auth_router, token_router]
