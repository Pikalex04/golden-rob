

def run(bot):
    @bot.hybrid_command(
        description='sends the tech tutorial', aliases=['tech_tutorial', 'tutorial'], brief='Utilities',
        help='`/tech`: sends the tutorial', usage='`/tech`')
    async def tech(ctx):
        await ctx.send('https://youtu.be/lxsLwWh5_ZQ')

