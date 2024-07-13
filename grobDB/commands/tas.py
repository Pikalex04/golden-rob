

def run(bot):
    @bot.hybrid_command(
        description='sends TAS resources', brief='Utilities', help='`/tas`: sends the resources', usage='`/tas`')
    async def tas(ctx):
        await ctx.send(
            '- Mario Kart DS TAS server: https://discord.gg/JHT8MJbK6k\n'
            '- Mario Kart DS TAS Best Known Times: https://docs.google.com/spreadsheets/d/'
            '1WIneB7ZyINp1gLGzvrnIpqRejNanGl_B7LmhdHMrCoY/edit?usp=sharing')
