

def run(bot):
    @bot.hybrid_command(
        description='sends the Characters and Karts Stats spreadsheet', brief='Utilities',
        aliases=['kart_stat', 'stat', 'stats'], help='`/kart_stats`: sends the spreadsheet', usage='`/kart_stats`')
    async def kart_stats(ctx):
        await ctx.send(
            'https://docs.google.com/spreadsheets/d/10sUVtu7x_hJLpjYpKytHuUdrqTTAheN0DfCulJD3S7M/edit?usp=sharing')
