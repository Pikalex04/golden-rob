from discord import ButtonStyle, Embed, SelectOption, TextStyle
from discord.ext.commands import BucketType, CommandOnCooldown, cooldown
from discord.ui import Modal, Select, TextInput, button as view_button, View
from random import choice

from better_functions import better_countries as bc, better_discord as bd, better_embeds as be, better_json as bj
from grobDB.common import check_profile


def update_profile(user, field, value):
    try:
        file = bj.json_load(f'grobDB/users/{user.id}/profile.json')
    except FileNotFoundError:
        file = check_profile(user.id)
    file[field] = value
    bj.json_dump(f'grobDB/users/{user.id}/profile.json', file)


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
        try:
            friend_codes = bj.json_load(f'grobDB/users/{interaction.user.id}/profile.json')['friend_codes']
        except (KeyError, FileNotFoundError):
            friend_codes = check_profile(interaction.user.id)
        if friend_codes:
            hide = False
            fields = [
                ['<:stable_connection_icon:1234126101513764875> Add Code',
                 'Add another Friend Code to the database'],
                ['<:custom_connection_icon:1234126100062535791> Edit Code',
                 'Edit one of your saved Friend Codes or change its details'],
                ['<:unstable_connection_icon:1234126098011263007> Delete Code',
                 'Delete one of your saved Friend Codes.']
            ]
            if len(friend_codes) == 5:
                fields = fields[1:]
                hide = True
            e = Embed(title='What do you want to do?')
            e.set_author(name='Edit Friend Codes',
                         icon_url='https://cdn.discordapp.com/emojis/1232707683199746099.png?size=256')
            for field in fields:
                e.add_field(name=field[0], value=field[1], inline=False)
            await interaction.response.edit_message(embed=e, view=FriendCodeMenu(hide=hide, ctx=self.ctx))
        else:
            await main_add_friend_func(interaction, self.ctx)


class ProfileMenu(ViewModel):
    @view_button(label='Bio', style=ButtonStyle.gray, emoji='<:singleplayer_icon:1233072103675138158>')
    async def bio_button(self, interaction, button):
        await interaction.response.send_modal(ModalMenu(
            title='Please enter your new bio!', ctx=self.ctx,
            inputs=[TextInput(style=TextStyle.long, label='New bio', required=True, max_length=200,
                              placeholder='Average MKDS Enjoyer')], func=bio_func))
        await interaction.message.delete()

    @view_button(label='Country', style=ButtonStyle.gray, emoji='<:red_team:1233070943384109077>')
    async def country_button(self, interaction, button):
        e = Embed(
            description=f'{interaction.user.mention}, please react to __**this message**__ with the flag emoji of your '
                        'country!')
        e.set_author(name='Edit Country', icon_url='https://cdn.discordapp.com/emojis/1233070943384109077.png?size=256')
        await interaction.response.send_message(embed=e)
        await interaction.message.delete()

        async def check(r, user):
            flag_check = True
            print(str(r.emoji))
            try:
                _ = bc.get_official_country(bc.letter_parser(str(r.emoji)).upper())
            except KeyError:
                flag_check = False
            return (r.message.created_at == await interaction.original_message().created_at and
                    user.id == interaction.user.id and flag_check)

        try:
            flag = await interaction.client.wait_for('reaction_add', timeout=60, check=check)
        except TimeoutError:
            await interaction.channel.send(embed=be.timeout_embed(interaction.user.mention))
        else:
            flag_code = bc.letter_parser(str(flag[0].emoji)).upper()
            update_profile(
                interaction.user, 'country', [bc.get_official_country(flag_code), f':flag_{flag_code.lower()}:'])
            response = await interaction.channel.send(
                embed=be.success_embed(f'{interaction.user.mention}, your country was updated successfully!'))
            await response.delete(delay=10)
        await interaction.delete_original_response()

    @view_button(label='Socials', style=ButtonStyle.gray, emoji='<:multiplayer_icon:1233072100223488040>')
    async def socials_button(self, interaction, button):
        await interaction.response.send_modal(ModalMenu(
            title='Please enter the link to your profile!', ctx=self.ctx,
            inputs=[TextInput(style=TextStyle.short, label='Link to your profile', max_length=100,
                              placeholder='https://')], func=socials_func))
        await interaction.message.delete()

    @view_button(label='Go back', style=ButtonStyle.blurple, emoji='<:settings_icon:1233072101808935013>')
    async def go_back_button(self, interaction, button):
        await go_back_func(interaction, self.ctx)


async def bio_func(modal, interaction):
    for word in modal.children[0].value.lower().split():
        if word in bj.json_load('grobDB/settings/ui_sanitizer.json'):
            await interaction.response.send_message(embed=be.error_embed(
                f'{interaction.user.mention}, that word is not allowed in a bio!'))
            break
    else:
        update_profile(interaction.user, 'bio', modal.children[0].value)
        await interaction.response.send_message(embed=be.success_embed(
            f'{interaction.user.mention}, your bio was updated successfully!'))


async def socials_func(modal, interaction):
    socials = bj.json_load('grobDB/settings/socials.json')
    for social in socials:
        for social_link in social[1]:
            if modal.children[0].value.lower().startswith(social_link):
                try:
                    existing_profiles = (bj.json_load(f'grobDB/users/{interaction.user.id}/profile.json'))['socials']
                except (KeyError, FileNotFoundError):
                    existing_profiles = check_profile(interaction.user.id)
                existing_profiles[social[2]] = modal.children[0].value
                update_profile(interaction.user, 'socials', existing_profiles)
                await interaction.response.send_message(embed=be.success_embed(
                    f'{interaction.user.mention}, your **{social[0]}** profile was updated successfully!'))
                return
    else:
        await interaction.response.send_message(embed=be.error_embed(
            f'{interaction.user.mention}, I couldn\'t recognize that link! '
            'Are you sure this Social Network is supported?\n'
            f'List of supported options: {", ".join(f"**{social[0]}**" for social in socials)}'))


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
            inputs=[TextInput(style=TextStyle.short, label='Your Players\' Page timesheet', min_length=46,
                              max_length=59, placeholder='https://www.mariokart64.com/mkds/profile.php?pid=')],
            func=rankings_func, special=[
                ['https://www.mariokart64.com/mkds/profile.php?pid=',
                 'https://mariokartplayers.com/mkds/profile.php?pid=',
                 'https://mariokart64.com/mkds/profile.php?pid=',
                 'https://www.mariokartplayers.com/mkds/profile.php?pid='], 'players_page', 'Players\' Page']))
        await interaction.message.delete()

    @view_button(label='speedrun.com', style=ButtonStyle.gray, emoji='<:speedruncom:1233054965388415126>')
    async def speedrun_com_button(self, interaction, button):
        await interaction.response.send_modal(ModalMenu(
            title='Please enter the link to your profile!', ctx=self.ctx,
            inputs=[TextInput(style=TextStyle.short, label='Your speedrun.com profile', min_length=27,
                              max_length=100, placeholder='https://speedrun.com/users/')],
            func=rankings_func, special=[['https://www.speedrun.com/users/', 'https://speedrun.com/users/'],
                                         'speedrun.com', 'speedrun.com']))
        await interaction.message.delete()

    @view_button(label='Cyberscore', style=ButtonStyle.gray, emoji='<:cyberscore:1233056528672489533>')
    async def cyberscore_button(self, interaction, button):
        await interaction.response.send_modal(ModalMenu(
            title='Please enter the link to your profile!', ctx=self.ctx,
            inputs=[TextInput(style=TextStyle.short, label='Your Cyberscore profile', min_length=31,
                              max_length=100, placeholder='https://cyberscore.me.uk/user/')],
            func=rankings_func, special=[['https://cyberscore.me.uk/user/', 'https://www.cyberscore.me.uk/user/'],
                                         'cyberscore', 'Cyberscore']))
        await interaction.message.delete()

    @view_button(label='Go back', style=ButtonStyle.blurple, emoji='<:settings_icon:1233072101808935013>')
    async def go_back_button(self, interaction, button):
        await go_back_func(interaction, self.ctx)


async def rankings_func(modal, interaction, special):
    for link in special[0]:
        if modal.children[0].value.lower().startswith(link):
            update_profile(interaction.user, special[1], modal.children[0].value)
            await interaction.response.send_message(embed=be.success_embed(
                f'{interaction.user.mention}, your {special[2]} profile was updated successfully!'))
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
    await interaction.message.delete()


async def add_friend_func(modal, interaction):
    code = ''.join(modal.children[0].value.split('-'))
    if not code.isdigit():
        await interaction.response.send_message(
            embed=be.error_embed(f'{interaction.user.mention}, a Friend Code can only include digits (0-9)!'))
    else:
        if not len(code) == 12:
            print('too long', code)
            await interaction.response.send_message(
                embed=be.error_embed(f'{interaction.user.mention}, that is not a valid Friend Code!'))
        else:
            code = code[:4] + '-' + code[4:8] + '-' + code[8:12]
            friend_codes = bj.json_load('grobDB/settings/fc.json')
            if code in friend_codes.keys():
                if friend_codes[code] == interaction.user.id:
                    await interaction.response.send_message(embed=be.error_embed(
                        f'{interaction.user.mention}, you have already saved that Friend Code!'))
                else:
                    await interaction.response.send_message(embed=be.error_embed(
                        f'{interaction.user.mention}, another user already has that Friend Code!'))
            else:
                try:
                    user_friend_codes = bj.json_load(f'grobDB/users/{interaction.user.id}/profile.json')['friend_codes']
                except (KeyError, FileNotFoundError):
                    user_friend_codes = check_profile(interaction.user.id)
                user_friend_codes.append([code, modal.children[1].value])
                update_profile(interaction.user, 'friend_codes', user_friend_codes)
                friend_codes[code] = interaction.user.id
                bj.json_dump('grobDB/settings/fc.json', friend_codes)
                await interaction.response.send_message(embed=be.success_embed(
                    f'{interaction.user.mention}, your Friend Code was updated successfully!'))


async def main_function_friend_func(interaction, label, func, ctx):
    options = []
    try:
        friend_codes = bj.json_load(f'grobDB/users/{interaction.user.id}/profile.json')['friend_codes']
    except (KeyError, FileNotFoundError):
        friend_codes = check_profile(interaction.user.id)
    for friend_code in friend_codes:
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
    if not modal.children[0].value:
        code = ''.join(modal.children[0].placeholder.split('-'))
    else:
        code = ''.join(modal.children[0].value.split('-'))
    if not code.isdigit():
        await interaction.response.send_message(
            embed=be.error_embed(f'{interaction.user.mention}, a Friend Code can only include digits (0-9)!'))
    else:
        if not len(code) == 12:
            await interaction.response.send_message(
                embed=be.error_embed(f'{interaction.user.mention}, that is not a valid Friend Code!'))
        else:
            friend_codes = bj.json_load('grobDB/settings/fc.json')
            code = code[:4] + '-' + code[4:8] + '-' + code[8:12]
            if code in friend_codes.keys() and code != modal.children[0].placeholder:
                if friend_codes[code] == interaction.user.id:
                    await interaction.response.send_message(embed=be.error_embed(
                        f'{interaction.user.mention}, you have already saved that Friend Code!'))
                else:
                    await interaction.response.send_message(embed=be.error_embed(
                        f'{interaction.user.mention}, another user already has that Friend Code!'))
            else:
                new_fc = [code, modal.children[1].value]
                if not modal.children[1].value:
                    new_fc[1] = modal.children[1].placeholder
                try:
                    user_friend_codes = bj.json_load(f'grobDB/users/{interaction.user.id}/profile.json')['friend_codes']
                except (KeyError, FileNotFoundError):
                    user_friend_codes = check_profile(interaction.user.id)
                user_friend_codes.remove([modal.children[0].placeholder, modal.children[1].placeholder])
                user_friend_codes.append(new_fc)
                update_profile(interaction.user, 'friend_codes', user_friend_codes)
                del friend_codes[modal.children[0].placeholder]
                friend_codes[new_fc[0]] = interaction.user.id
                bj.json_dump('grobDB/settings/fc.json', friend_codes)
                await interaction.response.send_message(embed=be.success_embed(
                    f'{interaction.user.mention}, your Friend Code was updated successfully!'))


async def edit_friend_code_function(select, interaction, ctx):
    try:
        friend_codes = bj.json_load(f'grobDB/users/{interaction.user.id}/profile.json')['friend_codes']
    except (KeyError, FileNotFoundError):
        friend_codes = check_profile(interaction.user.id)
    for friend_code in friend_codes:
        if friend_code[0] == select.values[0]:
            await interaction.response.send_modal(ModalMenu(
                title='Please edit the Friend Code!', ctx=ctx,
                inputs=[TextInput(style=TextStyle.short, label='Your Friend Code', min_length=12, max_length=23,
                                  placeholder=friend_code[0], required=False),
                        TextInput(style=TextStyle.short, label='Details about your Friend Code', max_length=25,
                                  placeholder=friend_code[1], required=False)],
                func=edit_code_func))
            await interaction.delete_original_response()


async def delete_friend_code_function(select, interaction, ctx):
    try:
        user_friend_codes = bj.json_load(f'grobDB/users/{interaction.user.id}/profile.json')['friend_codes']
    except (KeyError, FileNotFoundError):
        user_friend_codes = check_profile(interaction.user.id)
    for friend_code in user_friend_codes:
        if friend_code[0] == select.values[0]:
            user_friend_codes.remove(friend_code)
            update_profile(interaction.user, 'friend_codes', user_friend_codes)
            friend_codes = bj.json_load('grobDB/settings/fc.json')
            del friend_codes[friend_code[0]]
            bj.json_dump('grobDB/settings/fc.json', friend_codes)
            await ctx.send(embed=be.success_embed(
                f'{interaction.user.mention}, your Friend Code was deleted successfully!'))
    await interaction.message.delete()


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
