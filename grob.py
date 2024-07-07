from discord import Intents
from discord.ext import commands
import importlib
from os import listdir

from better_functions import better_json as bj

intents = Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=bj.json_load('grobDB/settings/prefix.json'), owner_ids=bj.json_load('grobDB/settings/mods.json'),
    case_insensitive=True, intents=intents)

for directory in ['grobDB/commands', 'grobDB/events']:
    for command in listdir(directory):
        if command.endswith('.py'):
            importlib.import_module(f'{directory[0]}robDB.{directory[7:]}.{command[:-3]}').run(bot)


bot.run(open('grobDB/settings/token.txt', 'r').readline())
