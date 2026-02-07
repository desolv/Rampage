from abc import ABC

import discord


class BaseModule(ABC):
    name: str
    required_modules: set[str]

    def __init__(self):
        self.bot: discord.Client = None

    async def setup(self) -> None:
        pass

    async def _setup(self) -> None:
        await self.setup()
        print(f"Module '{self.name}' setup complete")

    async def teardown(self) -> None:
        pass

    async def _teardown(self) -> None:
        await self.teardown()
        print(f"Module '{self.name}' teardown complete")
