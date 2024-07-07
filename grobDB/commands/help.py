from discord.ext import commands
from discord import Embed

from better_functions import better_discord as bd, better_embeds as be


def run(bot):
    class MyHelp(commands.MinimalHelpCommand):
        async def send_bot_help(self, mapping):
            e = Embed()
            e.set_author(
                name=f'Commands List', icon_url='https://cdn.discordapp.com/emojis/1233072101808935013.png?size=256')
            e.set_footer(text='Arguments marked with <angle brackets> are required.\n'
                              'Arguments marked with [square brackets} are optional.')
            fields = {'Profile': [], 'Online': [], 'Utilities': [], 'Rankings': [], 'Rating Game': [], 'Fun': []}
            emojis = {
                'Profile': '<:singleplayer_icon:1233072103675138158>', 'Online': '<:online_icon:1233445495473569993>',
                'Utilities': '<:star_icon:1235173336292659230>', 'Fun': '<:mission_pin:1242475746388349061>',
                'Rating Game': '<:race_finished:1232707068759244891>',
                'Rankings': '<:players_page:1233055656638943253>'}
            for cog, commands in mapping.items():
                for command in commands:
                    if command.brief != 'Moderation':
                        try:
                            fields[command.brief].append(command)
                        except KeyError:
                            fields[command.brief] = [command]
            for field in fields:
                if fields[field]:
                    listed_commands = ['']
                    fields[field] = sorted(fields[field], key=lambda item: item.name)
                    for command in fields[field]:
                        if len(listed_commands[-1]) + len(f'/{command.name}') > 25:
                            listed_commands[-1] = listed_commands[-1][:-1]
                            listed_commands.append(f'`/{command.name}` ')
                        else:
                            listed_commands[-1] += f'`/{command.name}` '
                    e.add_field(name=f'{emojis[field]} {field}', value='\n'.join(line for line in listed_commands))
            await self.get_destination().send(embed=e)

        async def send_command_help(self, command):
            e = Embed(title=f'/{command.name}', description=f'```{command.description}```')
            e.set_author(
                name=f'Commands Help', icon_url='https://cdn.discordapp.com/emojis/1233072101808935013.png?size=256')
            alias = command.aliases
            fields = [['***Usages***', command.help], ['***Examples***', command.usage]]
            if alias:
                fields = ['***Aliases***', ', '.join(f'`{alias}`' for alias in alias)] + fields
            for field in fields:
                e.add_field(name=field[0], value=field[1], inline=False)
            e.set_footer(text='Arguments marked with <angle brackets> are required.\n'
                              'Arguments marked with [square brackets} are optional.')
            await self.get_destination().send(embed=e)

        async def send_error_message(self, error):
            if error == 'Command "error" has no subcommands.':
                pass
            else:
                await bd.unknownError(self.context, bot)

        async def on_help_command_error(self, ctx, error):
            if isinstance(error, commands.CommandOnCooldown):
                await ctx.send(embed=be.error_embed(f'{ctx.author.mention}, wait a while before reusing the command!'))
            else:
                await bd.unknownError(ctx, bot)

    bot.help_command = MyHelp(command_attrs={
        'name': 'help', 'aliases': ['h'], 'cooldown': commands.CooldownMapping.from_cooldown(
            2, 5, commands.BucketType.user), 'brief': 'Utilities'})
