

def run(bot):
    @bot.hybrid_command(
        description='sends the CTGP Nitro speedrun charts', aliases=['ctgp-n', 'ctgp_n'], brief='Utilities',
        help='`/ctgp`: sends the CTGP Nitro charts', usage='`/ctgp`')
    async def ctgp(ctx):
        await ctx.send('https://www.speedrun.com/ctgp_nitro')

