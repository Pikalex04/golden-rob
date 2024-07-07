

def run(bot):
    @bot.hybrid_command(
        description='sends the Best Known Splits spreadsheet', brief='Utilities',
        help='`/bks`: sends the BKS spreadsheet', usage='`/bks`')
    async def bks(ctx):
        await ctx.send(
            'https://docs.google.com/spreadsheets/d/1K0qfq2QUMCEVqp1WJUuNwpWF5YBX3ngGIDPyOVVOSlE/edit?usp=sharing')
