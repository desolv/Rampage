import asyncio
from typing import cast

from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

from architecture.manager import ModuleManager
from modules.rampage.module import RampageModule

load_dotenv()

ENABLED_MODULES = ["example"]

GUILD_ENABLED_MODULES = {
    1398060488235024504: {"example"},
}


async def main():
    bot = commands.Bot(
        command_prefix="?",
        intents=Intents.all(),
    )

    module_manager = ModuleManager(bot, GUILD_ENABLED_MODULES)
    bot.module_manager = module_manager

    try:
        await module_manager.enable_modules(ENABLED_MODULES)

        rampage_module = cast(RampageModule, module_manager.enabled_modules["rampage"])
        await rampage_module.start()

    except Exception as error:
        print(f"Error during bot startup: {error}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
