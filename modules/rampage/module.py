import os

from architecture.base import BaseModule
from architecture.registry import register_module


@register_module
class RampageModule(BaseModule):
    name = "rampage"
    required_modules = set()

    def __init__(self):
        super().__init__()

    async def setup(self) -> None:
        pass

    async def start(self) -> None:
        await self.bot.start(os.getenv("DISCORD_TOKEN"))

    async def teardown(self) -> None:
        if self.bot:
            await self.bot.close()
