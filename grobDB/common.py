from discord import ButtonStyle, Embed
from discord.ui import Button, View
from math import ceil
from os import mkdir

from better_functions import better_embeds as be, better_json as bj


def check_profile(user_id):
    try:
        mkdir(f'grobDB/users/')
    except FileExistsError:
        pass
    try:
        mkdir(f'grobDB/users/{user_id}/')
    except FileExistsError:
        pass
    default_profile = bj.json_load('grobDB/settings/default_profile.json')
    bj.json_dump(f'grobDB/users/{user_id}/profile.json', default_profile)
    return default_profile


def check_exp(user_id):
    try:
        mkdir(f'grobDB/users/')
    except FileExistsError:
        pass
    try:
        mkdir(f'grobDB/users/{user_id}/')
    except FileExistsError:
        pass
    default_exp = bj.json_load('grobDB/settings/default_exp.json')
    bj.json_dump(f'grobDB/users/{user_id}/exp.json', default_exp)
    return default_exp


class ReWindButton(Button):
    def __init__(self, *, hide=None, data=None, page=None, formatting=None, pages=None, ctx=None):
        self.hide = hide
        self.data = data
        self.page = page
        self.formatting = formatting
        self.pages = pages
        self.ctx = ctx
        super().__init__(label='-100', style=ButtonStyle.gray, emoji='⏪', disabled=True if 0 in hide else False)

    async def callback(self, interaction):
        if self.page - 10 < 0:
            self.page = 1
        else:
            self.page -= 10
        e, hide = make_leaderboard(self.page, self.data, self.pages, self.formatting)
        await interaction.message.edit(embed=e, view=LeaderboardView(
            hide=hide, data=self.data, pages=self.pages, page=self.page, formatting=self.formatting, ctx=self.ctx))


class PreviousButton(Button):
    def __init__(self, *, hide=None, data=None, page=None, formatting=None, pages=None, ctx=None):
        self.hide = hide
        self.data = data
        self.page = page
        self.formatting = formatting
        self.pages = pages
        self.ctx = ctx
        super().__init__(label='-10', style=ButtonStyle.gray, emoji='◀', disabled=True if 0 in hide else False)

    async def callback(self, interaction):
        self.page -= 1
        e, hide = make_leaderboard(self.page, self.data, self.pages, self.formatting)
        await interaction.message.edit(embed=e, view=LeaderboardView(
            hide=hide, data=self.data, pages=self.pages, page=self.page, formatting=self.formatting, ctx=self.ctx))


class NextButton(Button):
    def __init__(self, *, hide=None, data=None, page=None, formatting=None, pages=None, ctx=None):
        self.hide = hide
        self.data = data
        self.page = page
        self.formatting = formatting
        self.pages = pages
        self.ctx = ctx
        super().__init__(label='+10', style=ButtonStyle.gray, emoji='▶', disabled=True if 1 in hide else False)

    async def callback(self, interaction):
        self.page += 1
        e, hide = make_leaderboard(self.page, self.data, self.pages, self.formatting)
        await interaction.message.edit(embed=e, view=LeaderboardView(
            hide=hide, data=self.data, pages=self.pages, page=self.page, formatting=self.formatting, ctx=self.ctx))


class ForwardButton(Button):
    def __init__(self, *, hide=None, data=None, page=None, formatting=None, pages=None, ctx=None):
        self.hide = hide
        self.data = data
        self.page = page
        self.formatting = formatting
        self.pages = pages
        self.ctx = ctx
        super().__init__(label='+100', style=ButtonStyle.gray, emoji='⏩', disabled=True if 1 in hide else False)

    async def callback(self, interaction):
        if self.page + 10 > len(self.pages) - 1:
            self.page = len(self.pages)
        else:
            self.page += 10
        e, hide = make_leaderboard(self.page, self.data, self.pages, self.formatting)
        await interaction.message.edit(embed=e, view=LeaderboardView(
            hide=hide, data=self.data, pages=self.pages, page=self.page, formatting=self.formatting, ctx=self.ctx))


class LeaderboardView(View):
    def __init__(self, *, timeout=60, ctx=None, hide=None, data=None, page=None, formatting=None, pages=None):
        self.ctx = ctx
        super().__init__(timeout=timeout)
        for button in [
            ReWindButton(ctx=ctx, hide=hide, data=data, page=page, formatting=formatting, pages=pages),
            PreviousButton(ctx=ctx, hide=hide, data=data, page=page, formatting=formatting, pages=pages),
            NextButton(ctx=ctx, hide=hide, data=data, page=page, formatting=formatting, pages=pages),
            ForwardButton(ctx=ctx, hide=hide, data=data, page=page, formatting=formatting, pages=pages)
        ]:
            self.add_item(button)

    async def on_timeout(self):
        self.clear_items()

    async def interaction_check(self, interaction):
        check = interaction.user.id == self.ctx.author.id
        await interaction.response.defer()
        return check


def make_leaderboard(page, data, pages, formatting):
    start_rank = (page - 1) * 10 + 1
    finish_rank = start_rank + 9
    e = Embed(
        title=data['title'], description=
        f'Viewing from {start_rank} to {finish_rank if finish_rank < len(data['times']) else len(data['times'])} out '
        f'of {len(data['times'])}')
    i = 1
    for score in pages[page - 1]:
        formatting(e, score)
        i += 1
    hide = []
    if page == 1:
        hide.append(0)
    if len(pages) == page:
        hide.append(1)
    return e, hide


async def pp_leaderboard(ctx, chart, start, formatting):
    if not bj.json_load(f'grobDB/ppDB/maintenance.json')['status']:
        data = bj.json_load(chart)
        pages = []
        for i in range(ceil(len(data['times']) / 10)):
            pages.append(data['times'][0 + i * 10:10 + i * 10])
        try:
            page = ceil(int(start) / 10)
        except Exception:
            page = 1
        else:
            if page > len(pages):
                page = len(pages)
            elif page < 1:
                page = 1
        e, hide = make_leaderboard(page, data, pages, formatting)
        await ctx.send(embed=e, view=LeaderboardView(
            hide=hide, data=data, pages=pages, page=page, formatting=formatting, ctx=ctx))
    else:
        await ctx.send(embed=be.error_embed(
            f'{ctx.author.mention}, the Players\' Page database is in maintenance right now! Please try again later.'))
