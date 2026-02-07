from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user} with {len(self.bot.guilds)} guild(s)")


async def setup(bot):
    await bot.add_cog(Events(bot))
