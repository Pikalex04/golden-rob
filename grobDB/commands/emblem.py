from discord import ButtonStyle, Embed
from discord.ext.commands import BucketType, CommandOnCooldown, cooldown
from discord.ui import button as view_button, View
from math import ceil
from time import time
from sqlite3 import connect, Error

from better_functions import better_discord as bd, better_embeds as be


async def random_emblem(bot, call):
    with connect('grobDB/emblem/emblem.db') as connection:
        sql = call
        cursor = connection.cursor()
        cursor.execute(sql)
        emblem = cursor.fetchone()
    if connection:
        connection.close()
    e = Embed(title=emblem[1], description=f'Made by {emblem[2]}')
    e.set_author(name='Emblem Galley', icon_url='https://cdn.discordapp.com/emojis/1242475746388349061.png?size=256')
    message = await bot.get_channel(1245070824910622811).fetch_message(emblem[4])
    e.set_image(url=message.attachments[0].url)
    e.set_footer(text=f'Submitted by {emblem[3]}')
    return [e, emblem[1], emblem[2]]


class EmblemView(View):
    def __init__(self, *, timeout=60, bot=None, ctx=None, author=None, character=None):
        self.bot = bot
        self.ctx = ctx
        self.cooldown = time()
        self.author = author
        self.character = character
        super().__init__(timeout=timeout)

    async def on_timeout(self):
        self.clear_items()

    async def interaction_check(self, interaction):
        check = interaction.user.id == self.ctx.author.id
        if not check:
            await interaction.response.defer()
        return check

    @view_button(label='Another one!', style=ButtonStyle.gray)
    async def random_button(self, interaction, button):
        await interaction.response.defer()
        cooldown = time()
        if cooldown > self.cooldown + 2:
            emblem = await random_emblem(self.bot, f''' SELECT * FROM emblems AS t1 JOIN (
                SELECT id FROM emblems ORDER BY RANDOM() LIMIT 1) as t2 ON t1.id=t2.id ''')
            self.author = emblem[2]
            self.character = emblem[1]
            await interaction.message.edit(embed=emblem[0])
            self.cooldown = time()
        else:
            cooldown = ceil(self.cooldown + 2 - cooldown)
            msg = await interaction.channel.send(embed=be.error_embed(
                f'{interaction.user.mention} wait {cooldown} seconds before requesting another emblem!'))
            await msg.delete(delay=cooldown)

    @view_button(label='Another by same author!', style=ButtonStyle.gray)
    async def author_button(self, interaction, button):
        await interaction.response.defer()
        cooldown = time()
        if cooldown > self.cooldown + 2:
            emblem = await random_emblem(self.bot, f''' SELECT * FROM emblems AS t1 JOIN (
                SELECT id FROM emblems WHERE author = "{self.author}" ORDER BY RANDOM() LIMIT 1) as t2 ON 
                t1.id=t2.id ''')
            self.author = emblem[2]
            self.character = emblem[1]
            await interaction.message.edit(embed=emblem[0])
            self.cooldown = time()
        else:
            cooldown = ceil(self.cooldown + 2 - cooldown)
            msg = await interaction.channel.send(embed=be.error_embed(
                f'{interaction.user.mention} wait {cooldown} seconds before requesting another emblem!'))
            await msg.delete(delay=cooldown)

    @view_button(label='Another of the same character!', style=ButtonStyle.gray)
    async def character_button(self, interaction, button):
        await interaction.response.defer()
        cooldown = time()
        if cooldown > self.cooldown + 2:
            emblem = await random_emblem(self.bot, f''' SELECT * FROM emblems AS t1 JOIN (
                SELECT id FROM emblems WHERE name = "{self.character}" ORDER BY RANDOM() LIMIT 1) as t2 ON 
                t1.id=t2.id ''')
            self.author = emblem[2]
            self.character = emblem[1]
            await interaction.message.edit(embed=emblem[0])
            self.cooldown = time()
        else:
            cooldown = ceil(self.cooldown + 2 - cooldown)
            msg = await interaction.channel.send(embed=be.error_embed(
                f'{interaction.user.mention} wait {cooldown} seconds before requesting another emblem!'))
            await msg.delete(delay=cooldown)


def run(bot):
    @bot.hybrid_command(
        description='shows a cool emblem', brief='Fun', help='`/emblem`: shows an emblem', usage='`/emblem`')
    @cooldown(1, 5, BucketType.user)
    async def emblem(ctx):
        emblem = await random_emblem(
            bot, f''' SELECT * FROM emblems AS t1 JOIN (SELECT id FROM emblems ORDER BY RANDOM() LIMIT 1) as t2 
                    ON t1.id=t2.id ''')
        await ctx.send(embed=emblem[0], view=EmblemView(bot=bot, ctx=ctx, character=emblem[1], author=emblem[2]))

    @emblem.error
    async def emblemError(ctx, error):
        if isinstance(error, CommandOnCooldown):
            await bd.cocError(ctx, emblem)
        elif isinstance(error, Error):
            await ctx.send(embed=be.error_embed(
                f'{ctx.author.mention}, there was an error accessing the database! Please try again!'))
        else:
            await bd.unknownError(ctx, bot)
