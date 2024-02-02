import abc
from pydantic import BaseModel


class AuthRepositoryInterface(abc.ABC):

    @abc.abstractmethod
    async def set_obj(self, obj_schema: BaseModel):
        ...

    @abc.abstractmethod
    async def get_obj(self, obj_id: int):
        ...

    @abc.abstractmethod
    async def get_all_obj(self):
        ...

    @abc.abstractmethod
    async def update_obj(self, obj_id: int, obj_schema: BaseModel):
        ...

    @abc.abstractmethod
    async def delete_obj(self, obj_id: int):
        ...