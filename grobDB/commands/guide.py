

def run(bot):
    @bot.hybrid_command(
        description='sends the guide for connecting online', aliases=['g'], brief='Online',
        help='`/guide`: sends the guide', usage='`/guide`')
    async def guide(ctx):
        await ctx.send(
            'https://docs.google.com/document/d/1f3PChwQig40UaiPXlh-Gi5CggGiBPzyrpiecLZlT8ZE/edit?usp=sharing')
