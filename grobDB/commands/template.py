

def run(bot):
    @bot.hybrid_command(
        description='sends a template for submitting to the Players\' Page', brief='Utilities',
        help='`/template`: sends the template', usage='`/template`')
    async def template(ctx):
        await ctx.send(
            'For **first**-time submissions:\n'
            '```\n'
            'Date: July 23, 2022\n'
            'Name: Silver Robert\n'
            'Country: Italy\n'
            'Region: Optional Town\n'
            'E-mail: optional@but_recommended.com\n'
            'Info: Optionally, the Average MKDS Enjoyer\n'
            '\n'
            'PRB:\n'
            'rMC1: 0:13:999 (https://youtu.be/t5bVkcEdfs0)\n'
            'rLC1: 1:17:847 / 0:24:999\n'
            '\n'
            'Non-PRB:\n'
            'F8C: 1:19:999 (https://youtu.be/4rmAnIYP7Po)\n'
            'RR: 2:04:420 / 0:40:220 (https://youtu.be/Vxkr6x6aKC8 both)\n'
            '\n'
            'Hello, I am new. Thanks for updating my times!\n'
            '```\n'
            '\n'
            'For new submissions:\n'
            '```\n'
            'Date: July 23, 2022\n'
            'Name: Silver Robert\n'
            '\n'
            'PRB:\n'
            'rMC1: 0:13:999 (https://youtu.be/t5bVkcEdfs0)\n'
            'rLC1: 1:17:847 / 0:24:999\n'
            '\n'
            'Non-PRB:\n'
            'F8C: 1:19:999 (https://youtu.be/4rmAnIYP7Po)\n'
            'RR: 2:04:420 / 0:40:220 (https://youtu.be/Vxkr6x6aKC8 both)\n'
            '\n'
            'Thanks for updating!\n'
            '```')
