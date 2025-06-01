from json import loads
from sqlite3 import connect

from discord import app_commands, Embed, User
from discord.ext.commands import Bot, BucketType, CommandOnCooldown, cooldown, errors

from better_functions import better_discord as bd, better_json as bj
from grobDB.common import check_profile


def run(bot: Bot):
    """
    Defines the profile command.

    Parameters
    ----------
    bot : discord.ext.commands.Bot
        The bot for which the command needs to be defined.

    Returns
    -------
    None
    """
    @bot.hybrid_command(
        description='shows your profile or someone else\'s', aliases=['pf'], brief='Profile',
        help='`/profile`: shows your profile\n'
             '`/profile [user]`: shows the user\'s profile',
        usage='`/profile` `/profile Pikalex04` `/profile 552615180450660360`')
    @app_commands.describe(user='user whose profile you want to check')
    @cooldown(5, 30, BucketType.user)
    async def profile(ctx, user: User = None):
        """
        Displays the profile of a user.

        Parameters
        ----------
        ctx : discord.ext.commands.Context
            The context in which the command was called.

        user : discord.User, optional
            The user whose profile needs to be displayed.

        Returns
        -------
        None
        """
        # Selection of the user to display
        if user is None:
            user = ctx.author
        else:
            check_profile(user.id)  # Makes sure the user is present in the database

        # Opens the database
        conn = connect("grobDB/usersDB/users.db")
        cursor = conn.cursor()

        # Retrieval and selection of the profile
        cursor.execute(
            "SELECT bio, country, flag, patreon, twitch, x, yt, pp, src, cs, fcs FROM profile WHERE id = ?",
            (user.id,)
        )
        data = cursor.fetchone()

        conn.close()

        ## Setup of the embed
        e = Embed(title=f'Profile of {user.display_name}', description=f'{data[2]} {user.mention}')
        e.set_thumbnail(url=user.display_avatar.url)

        # Inclusion of generic fields
        e.add_field(name='Bio', value=data[0] if data[0] != '' else 'Nothing interesting here!', inline=False)
        e.add_field(name='Players\' Page', value=data[7] if data[7] != 'Unranked' else data[7])
        e.add_field(name='speedrun.com',
                    value=f'[{data[8].split('/', 4)[-1]}]({data[8]})' if data[8] != 'No profile' else data[8])
        e.add_field(name='Cyberscore',
                    value=f'[{data[9].split('/', 4)[-1]}]({data[9]})' if data[9] != 'No profile' else data[9])

        # Formatting of Friend Codes
        user_friend_codes = loads(data[10])
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

        # Formatting of social profiles
        socials = bj.json_load('grobDB/settings/socials.json')
        display_socials = ''
        i = 3  # The ID where socials start
        for social in socials:
            try:
                if data[i]:
                    display_socials += f'- [{social[0]}]({data[i]})\n'
            except KeyError:
                pass
        e.add_field(
            name='Socials', value=display_socials if display_socials != '' else 'Nothing to show!', inline=False)

        ##

        await ctx.send(embed=e)

    @profile.error
    async def profile_error(ctx, error):
        """
        Handles errors related to the profile command.

        Parameters
        ----------
        ctx : discord.ext.commands.Context
            The context in which the command was called.

        error :
            The error that was raised.

        Returns
        -------
        None
        """
        if isinstance(error, errors.UserNotFound):
            await bd.unfError(ctx)
        elif isinstance(error, CommandOnCooldown):
            await bd.cocError(ctx, profile)
        else:
            await bd.unknownError(ctx, bot)
