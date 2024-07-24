

def run(bot):
    @bot.hybrid_command(
        description='sends Wi-Fi-related resources', brief='Utilities', help='`/wifi`: sends the resources',
        usage='`/wifi`', aliases=['wifi_strat', 'wifi-strat'])
    async def wifi(ctx):
        await ctx.send(
            '- Wi-Fi Strat site: https://w.atwiki.jp/wifistrat/\n'
            '- Wi-Fi player rankings: '
            'https://docs.google.com/spreadsheets/d/1dTlgR19SxckwxtRXHH54hCXxVny8WNp65HxoMimiFYQ/edit?usp=sharing')
