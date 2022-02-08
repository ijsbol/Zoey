import os
from dotenv import load_dotenv
load_dotenv()

from nextcord.ext import commands
from nextcord import (
    Embed,
    Colour
)

class ModerativeLogging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_log_channel_id = int(os.getenv('MESSAGE_LOG_CHANNEL_ID'))

    def formatList(self, needs_formatting):
        format_list = ['{:>3}' for item in needs_formatting] 
        s = '\n'.join(format_list)
        return s.format(*needs_formatting)

    def createMessageDeleteLogEmbed(self, message, bulk=False):
        message_log_embed = Embed(
            colour=Colour.dark_red() if bulk else Colour.red(),
            title=f"A message sent by '{message.author.name}' was deleted.",
            description=message.content
        )
        message_log_embed.set_footer(text=f"User ID: {message.author.id} | Message ID: {message.id}")
        if len(message.attachments) > 0:
            message_log_embed.add_field(
                name="Attachments", 
                value=self.formatList([f"[**{att.content_type.upper()}** (*{att.filename})]({att.url}*)" for att in message.attachments])
            )
        return message_log_embed

    def createMessageEditLogEmbed(self, old_message, new_message):
        message_log_embed = Embed(
            colour=Colour.yellow(),
            title=f"'{old_message.author.name}' has edited their message."
        )
        message_log_embed.set_footer(text=f"User ID: {old_message.author.id} | Message ID: {old_message.id}")
        message_log_embed.add_field(name="Before", value=old_message.content, inline=False)
        message_log_embed.add_field(name="After", value=new_message.content, inline=False)
        message_log_embed.add_field(name="Information", value=f"**[Click me to jump to the message]({old_message.jump_url})** | Sent in {old_message.channel.mention}", inline=False)
        return message_log_embed

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot and "ml-exempt" not in str(message.channel.topic):
            message_log_channel = self.bot.get_channel(self.message_log_channel_id)
            if message_log_channel is not None:
                message_log_embed = self.createMessageDeleteLogEmbed(message)
                await message_log_channel.send(embed=message_log_embed)

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        embeds_list = []
        for message in messages:
            if not message.author.bot and "ml-exempt" not in str(message.channel.topic):
                embeds_list.append(self.createMessageDeleteLogEmbed(message, bulk=True))
        message_log_channel = self.bot.get_channel(self.message_log_channel_id)
        if message_log_channel is not None:
            log_segments = [embeds_list[x:x+20] for x in range(0, len(embeds_list), 20)] # Splitting up the embeds_list into multiple seperate lists each being 20 messages long
            for log_segment in log_segments:
                await message_log_channel.send(embeds=log_segment) # Sending up to 20 messages (a log segment) per message, to reduce overal log messages sent

    @commands.Cog.listener()
    async def on_message_edit(self, old_message, new_message):
        if not old_message.author.bot and "ml-exempt" not in str(old_message.channel.topic):
            if old_message.content != new_message.content: # Weird nextcord issue causing on_message_edit event to fire when no edits were made :thinking:
                message_log_channel = self.bot.get_channel(self.message_log_channel_id)
                if message_log_channel is not None:
                    message_log_embed = self.createMessageEditLogEmbed(old_message, new_message)
                    await message_log_channel.send(embed=message_log_embed)

def setup(bot):
    bot.add_cog(ModerativeLogging(bot))