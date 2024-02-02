from fastapi import FastAPI
from src.router.base_router import get_router


app = FastAPI()
for route in get_router():
    app.include_router(router=route)
