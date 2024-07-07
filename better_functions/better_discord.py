from math import floor

from better_functions import better_embeds as be, better_json as bj


def block_dm(ctx):
    return ctx.guild is not None


async def ceError(ctx):
    await ctx.send(embed=be.error_embed(
        f'{ctx.author.mention}, `{ctx.prefix}{ctx.invoked_with}` cannot be used in DMs!'))


async def cocError(ctx, command):
    cooldown = floor(command.get_cooldown_retry_after(ctx))
    if cooldown > 60:
        cooldown = f'**{floor(cooldown / 60)}** minutes'
    else:
        cooldown = f'**{cooldown}** seconds'
    await ctx.send(embed=be.error_embed(
        f'{ctx.author.mention}, wait {cooldown} before using `{ctx.prefix}{ctx.invoked_with}` again!'))


async def mraError(ctx, args):
    if isinstance(args, str):
        await ctx.send(embed=be.error_embed(f'{ctx.author.mention}, you forgot to specify the argument `{args}`!'))
    else:
        await ctx.send(embed=be.error_embed(
            f'{ctx.author.mention}, you forgot to specify the following arguments:'
            f'{' `{}`'.format(arg for arg in args)}'))


async def unfError(ctx):
    await ctx.send(embed=be.error_embed(
        f'{ctx.author.mention}, I could not find that user! If you cannot type the user\'s name, try pasting their ID! '
        'This works even for users who share a server with the bot but aren\'t in this specific server. If you used '
        'an ID already, then the user has no connection to the bot whatsoever, so it cannot retrieve their data.'))


async def unknownError(ctx, bot):
    await ctx.send(embed=be.error_embed(f'{ctx.author.mention}, there was an unknown error while trying to run this '
                                        f'command! Please report to <@{bot.owner_ids[0]}>!'))
    await bot.get_channel(bj.json_load('grobDB/settings/mod_log.json')).send(
        f'<@552615180450660360>, unknown error in this message!\n{ctx.message.jump_url}')
