from discord import app_commands, Embed, User
from discord.ext.commands import BucketType, CommandOnCooldown, cooldown, errors

from better_functions import better_discord as bd, better_json as bj
from grobDB.common import check_profile


def run(bot):
    @bot.hybrid_command(
        description='shows your profile or someone else\'s', aliases=['pf'], brief='Profile',
        help='`/profile`: shows your profile\n'
             '`/profile [user]`: shows the user\'s profile',
        usage='`/profile` `/profile Pikalex04` `/profile 552615180450660360`')
    @app_commands.describe(user='user whose profile you want to check')
    @cooldown(5, 30, BucketType.user)
    async def profile(ctx, user: User = None):
        if user is None:
            user = ctx.author
        try:
            data = bj.json_load(f'grobDB/users/{user.id}/profile.json')
        except Exception:
            data = check_profile(user.id)
        e = Embed(title=f'Profile of {user.display_name}', description=f'{data["country"][1]} {user.mention}')
        socials = bj.json_load('grobDB/settings/socials.json')
        display_socials = ''
        for social in socials:
            try:
                if data['socials'][social[2]]:
                    display_socials += f'- [{social[0]}]({data['socials'][social[2]]})\n'
            except KeyError:
                pass
        e.set_thumbnail(url=user.display_avatar.url)
        e.add_field(name='Bio', value=data['bio'] if data['bio'] != '' else 'Nothing interesting here!', inline=False)
        e.add_field(
            name='Players\' Page',
            value=f'[{data["players_page"].split('=')[-1]}]({data["players_page"]})'
            if data['players_page'] != 'Unranked' else data['players_page'])
        e.add_field(
            name='speedrun.com',
            value=f'[{data["speedrun.com"].split('/', 4)[-1]}]({data["speedrun.com"]})'
            if data['speedrun.com'] != 'No profile' else data['speedrun.com'])
        e.add_field(
            name='Cyberscore',
            value=f'[{data["cyberscore"].split('/', 4)[-1]}]({data["cyberscore"]})'
            if data['cyberscore'] != 'No profile' else data['cyberscore'])
        user_friend_codes = data['friend_codes']
        if user_friend_codes:
            if len(user_friend_codes) > 1:
                e.add_field(name='Friend Codes',
                            value='\n'.join(f'- {friend_code[0]}'
                                            f'{f' ({friend_code[1]})' if friend_code[1] != '' else ''}'
                                            for friend_code in user_friend_codes))
            else:
                e.add_field(name='Friend Code',
                            value=f'{user_friend_codes[0][0]}'
                                  f'{f' ({user_friend_codes[0][1]})' if user_friend_codes[0][1] != '' else ''}')
        else:
            e.add_field(name='Friend Codes', value='None')
        e.add_field(
            name='Socials', value=display_socials if display_socials != '' else 'Nothing to show!', inline=False)
        await ctx.send(embed=e)

    @profile.error
    async def profileError(ctx, error):
        if isinstance(error, errors.UserNotFound):
            await bd.unfError(ctx)
        elif isinstance(error, CommandOnCooldown):
            await bd.cocError(ctx, profile)
        else:
            await bd.unknownError(ctx, bot)
