from discord.ext import commands


class ExampleCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="example")
    async def example_command(self, ctx: commands.Context) -> None:
        await ctx.send("Example module is working!")


async def setup(bot):
    await bot.add_cog(ExampleCommand(bot))
