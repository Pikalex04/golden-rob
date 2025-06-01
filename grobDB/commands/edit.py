from discord import ButtonStyle, Embed, SelectOption, TextStyle
from discord.ext.commands import BucketType, CommandOnCooldown, cooldown
from discord.ui import Modal, Select, TextInput, button as view_button, View
from json import dumps, loads
from random import choice
from sqlite3 import connect

from better_functions import better_countries as bc, better_discord as bd, better_embeds as be, better_json as bj
from grobDB.common import check_profile


def update_profile(user: int, column: str, data):
    """
    Updates the user's column with the new data.

    Parameters
    ----------
    user : int
        The user's ID.

    column : str
        The column to update.

    data :
        The data to add.

    Returns
    -------
    None
    """

    check_profile(user)  # Makes sure the user is present in the database

    # Opens the users database
    conn = connect("grobDB/usersDB/users.db")
    cursor = conn.cursor()

    # Updates the value
    cursor.execute(f"UPDATE profile SET {column} = ? WHERE id = ?", (data, user))
    conn.commit()

    conn.close()
    return


class ViewModel(View):
    def __init__(self, *, timeout=60, ctx=None):
        self.ctx = ctx
        super().__init__(timeout=timeout)

    async def on_timeout(self):
        self.clear_items()

    async def interaction_check(self, interaction):
        check = interaction.user.id == self.ctx.author.id
        if not check:
            await interaction.response.defer()
        return check


class ModalMenu(Modal):
    def __init__(self, inputs=None, title=None, option=None, func=None, special=None, ctx=None):
        self.func = func
        self.option = option
        self.special = special
        self.ctx = ctx
        super().__init__(title=title)
        for input in inputs:
            self.add_item(input)

    async def on_submit(self, interaction):
        if self.special is None:
            await self.func(self, interaction)
        else:
            await self.func(self, interaction, self.special)


class MainMenu(ViewModel):
    @view_button(label='Player Data', style=ButtonStyle.gray, emoji='<:rob:1232701955781165087>')
    async def data_button(self, interaction, button):
        e = Embed(title='What do you want to edit?')
        e.set_author(
            name='Edit Player Data', icon_url='https://cdn.discordapp.com/emojis/1232701955781165087.png?size=256')
        for field in [['<:singleplayer_icon:1233072103675138158> Bio',
                       'Add a little story about yourself (max. 200 characters)'],
                      ['<:red_team:1233070943384109077> Country',
                       'Add your country to display it.'],
                      ['<:multiplayer_icon:1233072100223488040> Socials',
                       'Add a link to one of your Social Network profiles.\n'
                       'List of supported options: '
                       f'{", ".join(f"**{social[0]}**" for social in bj.json_load("grobDB/settings/socials.json"))}.']]:
            e.add_field(name=field[0], value=field[1], inline=False)
        await interaction.response.edit_message(embed=e, view=ProfileMenu(ctx=self.ctx))

    @view_button(label='Rankings', style=ButtonStyle.gray, emoji='<:race_finished:1232707068759244891>')
    async def rankings_button(self, interaction, button):
        e = Embed(title='What do you want to edit?')
        e.set_author(
            name='Edit Rankings', icon_url='https://cdn.discordapp.com/emojis/1232701955781165087.png?size=256')
        for field in [
            ['<:players_page:1233055656638943253> Players\' Page',
             'Link your Time Trials timesheet (to work, your link has to end with `pid=` followed by a number).'],
            ['<:speedruncom:1233054965388415126> speedrun.com', 'Link your speedruns profile.'],
            ['<:cyberscore:1233056528672489533> Cyberscore',
             'Link your Cyberscore profile (Grand Prix and Mission Mode scores).']]:
            e.add_field(name=field[0], value=field[1], inline=False)
        await interaction.response.edit_message(embed=e, view=RankingsMenu(ctx=self.ctx))

    @view_button(label='Friend Code', style=ButtonStyle.gray, emoji='<:friend_online:1232707683199746099>')
    async def friend_code_button(self, interaction, button):
        """
        Defines what happens when the friend code button is pressed.
        If the user has any friend codes saved, it gets prompted with the options of adding a new one, editing one or
        deleting one.
        A user may add a friend code only if there are less than 5 friend codes already saved under its name.

        If the user doesn't have any friend codes yet, the button forwards to the function to add a new friend code.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction in which the button was pressed.

        button : discord.ui.Button
            The button that was pressed.

        Returns
        -------
        None
        """

        # Opens the users database
        conn = connect("grobDB/usersDB/users.db")
        cursor = conn.cursor()

        # Retrieval and selection of the user's friend codes
        cursor.execute("SELECT fcs FROM profile WHERE id = ?", (interaction.user.id,))
        friend_codes = loads(cursor.fetchone()[0])

        conn.close()

        # Checks if there are friend codes already present
        if friend_codes: # Creates the menu to select what to do with friend codes
            fields = [
                ['<:stable_connection_icon:1234126101513764875> Add Code',
                 'Add another Friend Code to the database'],
                ['<:custom_connection_icon:1234126100062535791> Edit Code',
                 'Edit one of your saved Friend Codes or change its details'],
                ['<:unstable_connection_icon:1234126098011263007> Delete Code',
                 'Delete one of your saved Friend Codes.']
            ]

            # If the user already has 5 friend codes, the option to add a new one is disabled
            if len(friend_codes) == 5:
                fields = fields[1:]
                hide = True
            else:
                hide = False

            # Set-up of the embed
            e = Embed(title='What do you want to do?')
            e.set_author(name='Edit Friend Codes',
                         icon_url='https://cdn.discordapp.com/emojis/1232707683199746099.png?size=256')
            for field in fields:
                e.add_field(name=field[0], value=field[1], inline=False)

            await interaction.response.edit_message(embed=e, view=FriendCodeMenu(hide=hide, ctx=self.ctx))
        else:
            await main_add_friend_func(interaction, self.ctx)  # Opens the menu to add a friend code


class ProfileMenu(ViewModel):
    @view_button(label='Bio', style=ButtonStyle.gray, emoji='<:singleplayer_icon:1233072103675138158>')
    async def bio_button(self, interaction, button):
        """
        Opens the menu for editing the bio.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction in which the button was pressed.

        button : discord.ui.Button
            The button that was pressed.

        Returns
        -------
        None
        """
        await interaction.response.send_modal(ModalMenu(
            title='Please enter your new bio!', ctx=self.ctx,
            inputs=[TextInput(style=TextStyle.long, label='New bio', required=False, max_length=200,
                              placeholder='Leave blank to remove...')], func=bio_func))
        return

    @view_button(label='Country', style=ButtonStyle.gray, emoji='<:red_team:1233070943384109077>')
    async def country_button(self, interaction, button):
        """
        Opens the menu for editing the country.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction in which the button was pressed.

        button : discord.ui.Button
            The button that was pressed.

        Returns
        -------
        None
        """

        # Sends the embed the user needs to react to with their country of preference
        e = Embed(
            description=f'{interaction.user.mention}, please react to __**this message**__ with the flag emoji of your '
                        'country! To remove your country, reach with ❌ instead.')
        e.set_author(name='Edit Country', icon_url='https://cdn.discordapp.com/emojis/1233070943384109077.png?size=256')
        await interaction.response.send_message(embed=e)
        await interaction.message.delete()

        creation_date = await interaction.original_response()
        creation_date = creation_date.created_at

        def check(r, user):
            """
            Checks that the message the user reacted to is correct and that it's the correct user the one who reacted.
            Returns the result of the check.

            Parameters
            ----------
            r: discord.Reaction
                The reaction that was received.

            user: discord.User
                The user who sent the reaction.

            Returns
            -------
            Boolean
            """

            flag_check = True  # Flag to check whether the emoji is valid

            # Checks if the user wants to remove the flag or not
            if str(r.emoji) == '❌':
                return r.message.created_at == creation_date and user.id == interaction.user.id and flag_check
            else:
                # Retrieves the country from the flag
                try:
                    _ = bc.get_official_country(bc.letter_parser(str(r.emoji)).upper())
                except KeyError:
                    flag_check = False

                return r.message.created_at == creation_date and user.id == interaction.user.id and flag_check

        # Waits for the user to react to the message
        try:
            flag = await interaction.client.wait_for('reaction_add', timeout=60, check=check)
        except TimeoutError:
            await interaction.channel.send(embed=be.timeout_embed(interaction.user.mention))
        else:
            if str(flag[0].emoji) == '❌':
                # Removes the country data
                update_profile(interaction.user.id, 'country', "Unknown")
                update_profile(interaction.user.id, 'flag', ":flag_white:")

                response = await interaction.channel.send(
                    embed=be.success_embed(f'{interaction.user.mention}, your country was updated successfully!'))
                await response.delete(delay=10)
            else:
                # Adds the country
                flag_code = bc.letter_parser(str(flag[0].emoji)).upper()
                update_profile(interaction.user.id, 'country', bc.get_official_country(flag_code))
                update_profile(interaction.user.id, 'flag', f':flag_{flag_code.lower()}:')

                response = await interaction.channel.send(
                    embed=be.success_embed(f'{interaction.user.mention}, your country was updated successfully!'))
                await response.delete(delay=10)
        await interaction.delete_original_response()
        return

    @view_button(label='Socials', style=ButtonStyle.gray, emoji='<:multiplayer_icon:1233072100223488040>')
    async def socials_button(self, interaction, button):
        """
        Opens the menu for editing the socials.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction in which the button was pressed.

        button : discord.ui.Button
            The button that was pressed.

        Returns
        -------
        None
        """
        await interaction.response.send_modal(ModalMenu(
            title='Please enter the link to your profile!', ctx=self.ctx,
            inputs=[TextInput(
                style=TextStyle.short, label='Link to your profile', max_length=100,
                placeholder='To remove a profile, set the domain URL with no user ID')], func=socials_func))
        return

    @view_button(label='Go back', style=ButtonStyle.blurple, emoji='<:settings_icon:1233072101808935013>')
    async def go_back_button(self, interaction, button):
        """
        Opens the previous menu.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction in which the button was pressed.

        button : discord.ui.Button
            The button that was pressed.

        Returns
        -------
        None
        """
        await go_back_func(interaction, self.ctx)
        return


async def bio_func(modal, interaction):
    await interaction.message.delete()
    response = modal.children[0].value.lower()
    if len(response) == 0:
        update_profile(interaction.user.id, 'bio', '')
        await interaction.response.send_message(embed=be.success_embed(
            f'{interaction.user.mention}, your bio was removed successfully!'))
    else:
        for word in response.split():
            if word in bj.json_load('grobDB/settings/ui_sanitizer.json'):
                await interaction.response.send_message(embed=be.error_embed(
                    f'{interaction.user.mention}, that word is not allowed in a bio!'))
                break
        else:
            update_profile(interaction.user.id, 'bio', response)
            await interaction.response.send_message(embed=be.success_embed(
                f'{interaction.user.mention}, your bio was updated successfully!'))


async def socials_func(modal, interaction):
    """
    Applies the selected action in the social menu.

    Parameters
    ----------
    modal: discord.ext.commands.Modal
        The modal of the menu.

    interaction: discord.ext.commands.Interaction
        The interaction through which the menu was called.

    Returns
    -------
    None
    """

    await interaction.message.delete()

    # Cycles through the available socials
    socials = bj.json_load('grobDB/settings/socials.json')
    response = modal.children[0].value.lower()
    for social in socials:
        for social_link in social[1]:
            # Checks if the response starts with the url of the current social
            if response.startswith(social_link):
                # Checks if the ID is empty to remove the social, else it adds the specified profile
                if len(response.split('/')[-1]) == 0:
                    update_profile(interaction.user.id, socials[2], '')

                    await interaction.response.send_message(embed=be.success_embed(
                        f'{interaction.user.mention}, your **{social[0]}** profile was removed successfully!'))
                else:
                    update_profile(interaction.user.id, socials[2], response)

                    await interaction.response.send_message(embed=be.success_embed(
                        f'{interaction.user.mention}, your **{social[0]}** profile was updated successfully!'))
                return
    else:
        await interaction.response.send_message(embed=be.error_embed(
            f'{interaction.user.mention}, I couldn\'t recognize that link! '
            'Are you sure this Social Network is supported?\n'
            f'List of supported options: {", ".join(f"**{social[0]}**" for social in socials)}'))
    return


async def go_back_func(interaction, ctx):
    e = Embed(title='What do you want to edit?')
    e.set_author(name='Edit profile', icon_url='https://cdn.discordapp.com/emojis/1233072101808935013.png?size=256')
    for field in [['<:rob:1232701955781165087> Player Data', 'Includes Bio, Country and Main Socials'],
                  ['<:race_finished:1232707068759244891> Rankings',
                   'Includes links to the player\'s rankings pages'],
                  ['<:friend_online:1232707683199746099> Friend Code',
                   'Add your Friend Code to the database']]:
        e.add_field(name=field[0], value=field[1], inline=False)
    await interaction.response.edit_message(embed=e, view=MainMenu(ctx=ctx))


class RankingsMenu(ViewModel):
    @view_button(label='Players\' Page', style=ButtonStyle.gray, emoji='<:players_page:1233055656638943253>')
    async def players_page_button(self, interaction, button):
        await interaction.response.send_modal(ModalMenu(
            title='Please enter the link to your timesheet!', ctx=self.ctx,
            inputs=[TextInput(
                style=TextStyle.short, label='Leave blank if you want to remove...', max_length=59,
                placeholder='https://www.mariokart64.com/mkds/profile.php?pid=', required=False)],
            func=rankings_func, special=[
                ['https://www.mariokart64.com/mkds/profile.php?pid=',
                 'https://mariokartplayers.com/mkds/profile.php?pid=',
                 'https://mariokart64.com/mkds/profile.php?pid=',
                 'https://www.mariokartplayers.com/mkds/profile.php?pid='], 'pp', 'Players\' Page']))

    @view_button(label='speedrun.com', style=ButtonStyle.gray, emoji='<:speedruncom:1233054965388415126>')
    async def speedrun_com_button(self, interaction, button):
        await interaction.response.send_modal(ModalMenu(
            title='Please enter the link to your profile!', ctx=self.ctx,
            inputs=[TextInput(
                style=TextStyle.short, label='Leave blank if you want to remove...', max_length=100,
                placeholder='https://speedrun.com/users/', required=False)],
            func=rankings_func, special=[['https://www.speedrun.com/users/', 'https://speedrun.com/users/'],
                                         'src', 'speedrun.com']))

    @view_button(label='Cyberscore', style=ButtonStyle.gray, emoji='<:cyberscore:1233056528672489533>')
    async def cyberscore_button(self, interaction, button):
        await interaction.response.send_modal(ModalMenu(
            title='Please enter the link to your profile!', ctx=self.ctx,
            inputs=[TextInput(
                style=TextStyle.short, label='Leave blank if you want to remove...', max_length=100,
                placeholder='https://cyberscore.me.uk/user/', required=False)],
            func=rankings_func, special=[['https://cyberscore.me.uk/user/', 'https://www.cyberscore.me.uk/user/'],
                                         'cs', 'Cyberscore']))

    @view_button(label='Go back', style=ButtonStyle.blurple, emoji='<:settings_icon:1233072101808935013>')
    async def go_back_button(self, interaction, button):
        await go_back_func(interaction, self.ctx)


async def rankings_func(modal, interaction, special):
    await interaction.message.delete()
    response = modal.children[0].value
    if len(response) == 0:
        update_profile(interaction.user.id, special[1], 'No profile')
        await interaction.response.send_message(embed=be.success_embed(
            f'{interaction.user.mention}, your {special[2]} profile was removed successfully!'))
    else:
        for link in special[0]:
            try:
                if response.lower().startswith(link) and len(response.split('/')[-1]) > 0:
                    update_res = response
                    if special[1] == 'pp':
                        if int(response.split('=')[-1]) > 0:
                            split_res = response.lower().split('?')[-1]
                            try:
                                pp_db = bj.json_load('grobDB/ppDB/stats/players.json')
                            except FileNotFoundError:
                                update_res = f'[{split_res[3:]}]({response})'
                            else:
                                for player in pp_db['times']:
                                    if player['info'].split('?')[-1] == split_res:
                                        update_res = f'[{player['player']}]({response})'
                                        break
                                else:
                                    update_res = f'[{split_res[3:]}]({response})'
                        else:
                            raise ValueError
                    update_profile(interaction.user.id, special[1], update_res)
                    await interaction.response.send_message(embed=be.success_embed(
                        f'{interaction.user.mention}, your {special[2]} profile was updated successfully!'))
                    break
            except ValueError:
                await interaction.response.send_message(embed=be.error_embed(
                    f'{interaction.user.mention}, that is not a {special[2]} profile!'))
                break
        else:
            await interaction.response.send_message(embed=be.error_embed(
                f'{interaction.user.mention}, that is not a {special[2]} profile!'))


class FriendCodeMenu(ViewModel):
    def __init__(self, hide=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hide:
            self.remove_item(self.children[0])

    @view_button(label='Add Code', style=ButtonStyle.gray, emoji='<:stable_connection_icon:1234126101513764875>')
    async def add_friend_code_button(self, interaction, button):
        await main_add_friend_func(interaction, self.ctx)

    @view_button(label='Edit Code', style=ButtonStyle.gray, emoji='<:custom_connection_icon:1234126100062535791>')
    async def edit_friend_code_button(self, interaction, button):
        await main_function_friend_func(
            interaction, 'Select the Friend Code you want to edit!', edit_friend_code_function, self.ctx)

    @view_button(label='Delete Code', style=ButtonStyle.gray, emoji='<:unstable_connection_icon:1234126098011263007>')
    async def delete_friend_code_button(self, interaction, button):
        await main_function_friend_func(
            interaction, 'Select the Friend Code you want to delete!', delete_friend_code_function, self.ctx)

    @view_button(label='Go back', style=ButtonStyle.blurple, emoji='<:settings_icon:1233072101808935013>')
    async def go_back_button(self, interaction, button):
        await go_back_func(interaction, self.ctx)


async def main_add_friend_func(interaction, ctx):
    await interaction.response.send_modal(ModalMenu(
        title='Please send your Friend Code in any format!', ctx=ctx,
        inputs=[TextInput(style=TextStyle.short, label='Your Friend Code', min_length=12, max_length=23,
                          placeholder='0000-0000-0000'),
                TextInput(style=TextStyle.short, label='Details about your Friend Code', max_length=25,
                          placeholder=choice(['Nintendo 3DS', 'melonDS', 'CTGP Nitro', 'Capture Card DS']),
                          required=False)],
        func=add_friend_func))


async def add_friend_func(modal, interaction):
    """
    Adds a friend code to the user's profile and the friend codes database.

    Parameters
    ----------
    modal: discord.ext.commands.Modal
        The modal of the menu.

    interaction: discord.ext.commands.Interaction
        The interaction through which the menu was called.

    Returns
    -------
    None
    """
    await interaction.message.delete()

    # Checks that the friend code is formatted properly
    code = ''.join(modal.children[0].value.split('-'))
    if not code.isdigit():
        await interaction.response.send_message(
            embed=be.error_embed(f'{interaction.user.mention}, a Friend Code can only include digits (0-9)!'))
    else:
        # Checks that the friend code is in the correct format
        if not len(code) == 12:
            await interaction.response.send_message(
                embed=be.error_embed(f'{interaction.user.mention}, that is not a valid Friend Code!'))
        else:
            code = code[:4] + '-' + code[4:8] + '-' + code[8:12]  # Formats the friend code properly

            # Opens the friend codes database
            fcs_conn = connect("grobDB/usersDB/fcs.db")
            fcs_cursor = fcs_conn.cursor()

            # Checks if the friend code is already assigned to a user
            fcs_cursor.execute("SELECT fc, user FROM fc WHERE fc = ?", (code,))
            data = fcs_cursor.fetchone()
            if data:
                if data[1] == interaction.user.id:
                    await interaction.response.send_message(embed=be.error_embed(
                        f'{interaction.user.mention}, you have already saved that Friend Code!'))
                else:
                    await interaction.response.send_message(embed=be.error_embed(
                        f'{interaction.user.mention}, another user already has that Friend Code!'))
            else:
                # Opens the friend codes database
                conn = connect("grobDB/usersDB/users.db")
                cursor = conn.cursor()

                # Retrieves the user's friend codes
                cursor.execute("SELECT fcs FROM profile WHERE id = ?", (interaction.user.id,))
                data = loads(cursor.fetchone()[0])
                conn.close()

                # Defaults the friend codes to [] if they weren't found in the database
                if not data:
                    data = []

                # Updates the friend codes
                data.append([code, modal.children[1].value])
                update_profile(interaction.user.id, 'fcs', dumps(data))
                fcs_cursor.execute("INSERT INTO fc (user, fc) VALUES (?, ?)", (interaction.user.id, code))
                fcs_conn.commit()
                await interaction.response.send_message(embed=be.success_embed(
                    f'{interaction.user.mention}, your Friend Code was updated successfully!'))

            fcs_conn.close()
    return


async def main_function_friend_func(interaction, label, func, ctx):
    """
    Creates the menu from which a friend code can be selected.

    Parameters
    ----------
    interaction: discord.ext.commands.Interaction
        The interaction through which the menu was called.

    label: str
        The label for the menu.

    func: function
        The function for the menu.

    ctx: discord.ext.commands.Context
        The context for the menu.

    Returns
    -------
    None
    """
    # Opens the friend codes database
    conn = connect("grobDB/usersDB/users.db")
    cursor = conn.cursor()

    # Checks if the friend code is already assigned to a user
    cursor.execute("SELECT fcs FROM profile WHERE id = ?", (interaction.user.id,))
    data = loads(cursor.fetchone()[0])
    conn.close()

    # Defaults the friend codes to [] if they weren't found in the database
    if not data:
        data = []

    # Adds the friend codes to the options
    options = []
    for friend_code in data:
        options.append(SelectOption(label=friend_code[0], description=friend_code[1]))

    await interaction.channel.send(
        view=FunctionFriendCodeMenu(
            func=FunctionFriendCodeSelect(placeholder=label, options=options, func=func, ctx=ctx), ctx=ctx))
    await interaction.message.delete()


class FunctionFriendCodeSelect(Select):
    def __init__(self, *, placeholder=None, func=None, options=None, ctx=None):
        self.func = func
        self.ctx = ctx
        super().__init__(placeholder=placeholder, options=options)

    async def callback(self, interaction):
        await self.func(self, interaction, self.ctx)


class FunctionFriendCodeMenu(ViewModel):
    def __init__(self, func=None, *args, **kwargs):
        super().__init__(*args, **kwargs, timeout=60)
        self.add_item(func)


async def edit_code_func(modal, interaction):
    """
    Edits the user's friend code.

    Parameters
    ----------
    modal: discord.ext.commands.Modal
        The modal of the edit menu.

    interaction: discord.ext.commands.Interaction
        The interaction through which the menu was called.

    Returns
    -------
    None
    """
    if not modal.children[0].value:
        code = ''.join(modal.children[0].placeholder.split('-'))
    else:
        code = ''.join(modal.children[0].value.split('-'))

    # Checks that the friend code is formatted properly
    if not code.isdigit():
        await interaction.response.send_message(
            embed=be.error_embed(f'{interaction.user.mention}, a Friend Code can only include digits (0-9)!'))
    else:
        if not len(code) == 12:
            await interaction.response.send_message(
                embed=be.error_embed(f'{interaction.user.mention}, that is not a valid Friend Code!'))
        else:
            code = code[:4] + '-' + code[4:8] + '-' + code[8:12]  # Formats the friend code properly

            # Opens the friend codes database
            fcs_conn = connect("grobDB/usersDB/fcs.db")
            fcs_cursor = fcs_conn.cursor()

            # Checks if the friend code is already assigned to a user
            fcs_cursor.execute("SELECT fc, user FROM fc WHERE fc = ?", (code,))
            data = fcs_cursor.fetchone()

            # Checks that the friend code is valid
            if data and code != modal.children[0].placeholder:
                if data[1] == interaction.user.id:
                    await interaction.response.send_message(embed=be.error_embed(
                        f'{interaction.user.mention}, you have already saved that Friend Code!'))
                else:
                    await interaction.response.send_message(embed=be.error_embed(
                        f'{interaction.user.mention}, another user already has that Friend Code!'))
            else:
                new_fc = [code, modal.children[1].value]
                if not modal.children[1].value:
                    new_fc[1] = modal.children[1].placeholder

                # Opens the friend codes database
                conn = connect("grobDB/usersDB/users.db")
                cursor = conn.cursor()

                # Checks if the friend code is already assigned to a user
                cursor.execute("SELECT fcs FROM profile WHERE id = ?", (interaction.user.id,))
                data = loads(cursor.fetchone()[0])
                conn.close()

                data.remove([modal.children[0].placeholder, modal.children[1].placeholder])  # Removes the friend code
                data.append(new_fc)  # Adds the new one

                # Updates the databases
                update_profile(interaction.user.id, 'fcs', dumps(data))
                fcs_cursor.execute("UPDATE fc SET fc = ? WHERE user = ?", (code, interaction.user.id))
                fcs_cursor.execute("DELETE FROM fc WHERE fc = ?", (modal.children[0].placeholder,))
                fcs_conn.commit()
                await interaction.response.send_message(embed=be.success_embed(
                    f'{interaction.user.mention}, your Friend Code was updated successfully!'))

            fcs_conn.close()
    return



async def edit_friend_code_function(select, interaction, ctx):
    """
    Builds the menu for editing a friend code.

    Parameters
    ----------
    select:
        The selected friend code.

    interaction: discord.ext.commands.Interaction
        The interaction through which the menu was called.

    ctx: discord.ext.commands.Context
        The context through which the menu was called.

    Returns
    -------
    None
    """
    # Opens the friend codes database
    conn = connect("grobDB/usersDB/users.db")
    cursor = conn.cursor()

    # Checks if the friend code is already assigned to a user
    cursor.execute("SELECT fcs FROM profile WHERE id = ?", (interaction.user.id,))
    data = loads(cursor.fetchone()[0])
    conn.close()

    # Cycles through the user's friend codes to find the selected one
    for friend_code in data:
        if friend_code[0] == select.values[0]:
            await interaction.response.send_modal(ModalMenu(
                title='Please edit the Friend Code!', ctx=ctx,
                inputs=[TextInput(style=TextStyle.short, label='Your Friend Code', min_length=12, max_length=23,
                                  placeholder=friend_code[0], required=False),
                        TextInput(style=TextStyle.short, label='Details about your Friend Code', max_length=25,
                                  placeholder=friend_code[1], required=False)],
                func=edit_code_func))
    return


async def delete_friend_code_function(select, interaction, ctx):
    """
    Deletes the user's friend code.

    Parameters
    ----------
    select:
        The selected friend code.

    interaction: discord.ext.commands.Interaction
        The interaction through which the menu was called.

    ctx: discord.ext.commands.Context
        The context through which the menu was called.

    Returns
    -------
    None
    """
    # Opens the friend codes database
    conn = connect("grobDB/usersDB/users.db")
    cursor = conn.cursor()

    # Checks if the friend code is already assigned to a user
    cursor.execute("SELECT fcs FROM profile WHERE id = ?", (interaction.user.id,))
    data = loads(cursor.fetchone()[0])
    conn.close()

    # Cycles through the user's friend codes to find the selected one
    for friend_code in data:
        if friend_code[0] == select.values[0]:
            # Removes the friend code from the profile
            data.remove(friend_code)
            update_profile(interaction.user.id, 'fcs', dumps(data))

            # Updates the friend codes database
            fcs_conn = connect("grobDB/usersDB/fcs.db")
            fcs_cursor = fcs_conn.cursor()
            fcs_cursor.execute("DELETE FROM fc WHERE fc = ?", (friend_code[0],))
            fcs_conn.commit()
            fcs_conn.close()

            await ctx.send(embed=be.success_embed(
                f'{interaction.user.mention}, your Friend Code was deleted successfully!'))

    await interaction.message.delete()
    return


def run(bot):
    @bot.hybrid_command(
        description='edits your Mario Kart DS profile', brief='Profile', help='`/edit`: edits your profile',
        usage='`/edit`')
    @cooldown(3, 60, BucketType.user)
    async def edit(ctx):
        e = Embed(title='What do you want to edit?')
        e.set_author(name='Edit profile', icon_url='https://cdn.discordapp.com/emojis/1233072101808935013.png?size=256')
        for field in [['<:rob:1232701955781165087> Player Data', 'Includes Bio, Country and Main Socials'],
                      ['<:race_finished:1232707068759244891> Rankings',
                       'Includes links to the player\'s rankings pages'],
                      ['<:friend_online:1232707683199746099> Friend Code',
                       'Add your Friend Code to the database']]:
            e.add_field(name=field[0], value=field[1], inline=False)
        await ctx.send(embed=e, view=MainMenu(ctx=ctx))

    @edit.error
    async def editError(ctx, error):
        if isinstance(error, CommandOnCooldown):
            await bd.cocError(ctx, edit)
        else:
            await bd.unknownError(ctx, bot)