from abc import ABC, abstractmethod


class StorageProvider(ABC):
    @abstractmethod
    async def startup(self) -> None:
        ...

    async def __call__(self):
        ...
