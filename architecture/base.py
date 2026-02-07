from abc import ABC, abstractmethod

import discord


class BaseModule(ABC):
    name: str
    required_modules: set[str]

    def __init__(self):
        self.bot: discord.Client = None

    @abstractmethod
    async def setup(self) -> None:
        pass

    @abstractmethod
    async def teardown(self) -> None:
        pass
