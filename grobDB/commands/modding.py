

def run(bot):
    @bot.hybrid_command(
        description='sends the link to the MKDS Modding server', brief='Utilities', help='`/modding`: sends the invite',
        usage='`/modding`')
    async def modding(ctx):
        await ctx.send('https://discordapp.com/invite/CAktUYP')
