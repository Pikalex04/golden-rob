from discord import app_commands, Embed
from discord.ext.commands import BucketType, CommandOnCooldown, cooldown, MissingRequiredArgument, Range
from discord.ext.commands.errors import RangeError

from better_functions import better_discord as bd, better_embeds as be, better_json as bj


def run(bot):
    @bot.hybrid_command(
        description='shows details about an error code and solutions to solve it', aliases=['e'], brief='Online',
        help='`/error <error>`: shows details about that error', usage='`/error 86420` `/error 85020`')
    @app_commands.describe(error='the error you want to check')
    @cooldown(5, 20, BucketType.user)
    async def error(ctx, error: Range[int, 10000, 99999]):
        error_codes = bj.json_load('grobDB/settings/errors.json')
        try:
            fields = error_codes[str(error)]
        except KeyError:
            await ctx.send(embed=be.error_embed(f'{ctx.author.mention}, I could not find that error!'))
        else:
            e = Embed()
            e.set_author(name=f'Error Code {error}',
                         icon_url='https://cdn.discordapp.com/emojis/1234126098011263007.png?size=256')
            for field in fields:
                e.add_field(name=field[0], value=field[1], inline=False)
            await ctx.send(embed=e)

    @error.error
    async def errorError(ctx, error):
        if isinstance(error, CommandOnCooldown):
            await bd.cocError(ctx, error)
        elif isinstance(error, MissingRequiredArgument):
            await bd.mraError(ctx, 'error code')
        elif isinstance(error, RangeError):
            await ctx.send(embed=be.error_embed(
                f'{ctx.author.mention}, the error code has to be within the range of 10000 and 99999!'))
        else:
            await bd.unknownError(ctx, bot)