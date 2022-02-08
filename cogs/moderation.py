from nextcord.ext import commands
from nextcord import (
    Embed,
    Colour,
    Member,
    Forbidden
)

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def parsePunishmentMessages(self, punishment_dm, member, moderator, server, reason):
        punishment_dm = punishment_dm.replace("$user:mention", str(member.mention))
        punishment_dm = punishment_dm.replace("$user:name", str(member.name))
        punishment_dm = punishment_dm.replace("$user:id", str(member.id))
        punishment_dm = punishment_dm.replace("$user:discriminator", str(member.discriminator))

        punishment_dm = punishment_dm.replace("$server:name", str(server.name))
        punishment_dm = punishment_dm.replace("$server:id", str(server.id))

        punishment_dm = punishment_dm.replace("$moderator:mention", str(moderator.mention))
        punishment_dm = punishment_dm.replace("$moderator:name", str(moderator.name))
        punishment_dm = punishment_dm.replace("$moderator:id", str(moderator.id))
        punishment_dm = punishment_dm.replace("$moderator:discriminator", str(moderator.discriminator))

        punishment_dm = punishment_dm.replace("$reason", str(reason))

        return punishment_dm

    @commands.has_permissions(kick_members=True)
    @commands.command(aliases=[])
    async def kick(self, ctx, member: Member, *, reason="No reason provided."):
        punishment_dm = self.parsePunishmentMessages(self.bot.kick_message_raw, member, ctx.author, ctx.guild, reason)
        try:
            await member.send(punishment_dm)
            extra = "User was notified via DMs"
        except Forbidden:
            extra = "I was unable to DM this user"
        try:
            await member.kick(reason=f"Mod: {ctx.author.id} ({ctx.author}) | Reason: {reason}")
        except Forbidden:
            return await ctx.send(f"`📛` | I was unable to kick that user.")
        await ctx.send(f"`🐛` | **{member}** has been kicked. ({extra})")

    @commands.has_permissions(ban_members=True)
    @commands.command(aliases=[])
    async def ban(self, ctx, member: Member, *, reason="No reason provided."):
        punishment_dm = self.parsePunishmentMessages(self.bot.ban_message_raw, member, ctx.author, ctx.guild, reason)
        try:
            await member.send(punishment_dm)
            extra = "User was notified via DMs"
        except Forbidden:
            extra = "I was unable to DM this user"
        try:
            await member.kick(reason=f"Mod: {ctx.author.id} ({ctx.author}) | Reason: {reason}")
        except Forbidden:
            return await ctx.send(f"`📛` | I was unable to ban that user.")
        await ctx.send(f"`🐛` | **{member}** has been banned. ({extra})")

def setup(bot):
    bot.add_cog(Moderation(bot))