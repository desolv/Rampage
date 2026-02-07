from typing import Callable

from discord.ext import commands


def module_enabled(module_name: str) -> Callable:
    async def predicate(ctx: commands.Context) -> bool:
        if ctx.guild is None:
            raise commands.CheckFailure(f"Module '{module_name}' can only be used in guilds")

        module_manager = ctx.bot.module_manager

        if not module_manager.is_enabled_for_guild(module_name, ctx.guild.id):
            raise commands.CheckFailure(
                f"Module '{module_name}' is not enabled for this guild"
            )

        return True

    return commands.check(predicate)
