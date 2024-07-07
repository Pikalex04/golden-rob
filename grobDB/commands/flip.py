from discord import Embed
from random import choice


def run(bot):
    @bot.hybrid_command(description='flips a coin', brief='Fun', help='`/flip`: flips a coin', usage='`/flip`')
    async def flip(ctx):
        chosen = choice([[
            "head", '<:shine_runners_icon:1239645894203277425>'],
            ["tail", '<:reverse_shine_runners_icon:1239647764623921285>']])
        await ctx.send(embed=Embed(
            description=f'{chosen[1]} | ... got **{chosen[0]}**!'))
