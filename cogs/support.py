from nextcord.ext import commands

class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(case_insensitive=True)
    @commands.guild_only()
    async def tag(self, ctx):
        if (ctx.invoked_subcommand is None): None
    
    @tag.command()
    @commands.guild_only()
    async def create(self, ctx, name):
        await ctx.send("Coming soon")

def setup(bot):
    bot.add_cog(Support(bot))