from discord import Intents
from discord.ext import commands
from discord_slash import SlashCommand

bot = commands.Bot(command_prefix=".redundant",intents=Intents(messages=True, guilds=True, members=True, typing=True, presences=False))
slash = SlashCommand(bot, override_type = True, sync_commands=True)

bot.load_extension("wikicogs.base_cmds")
bot.run(open('tokens/wiki','r').read())
