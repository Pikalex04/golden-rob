

def run(bot):
    @bot.hybrid_command(
        description='sends CTGP Nitro-related resources', aliases=['ctgp-n', 'ctgp_n'], brief='Utilities',
        help='`/ctgp`: sends the CTGP-N resources', usage='`/ctgp`')
    async def ctgp(ctx):
        await ctx.send(
            '- Rankings: https://www.speedrun.com/ctgp_nitro\n'
            '- Patcher to **download** CTGP Nitro 1.1.0: https://ermelber.github.io/CTGPNitroWebPatcher/\n'
            '- Downloads for legacy versions (0.0.1, TT Edition and 1.0.0): '
            'https://www.speedrun.com/ctgp_nitro/resources\n'
            '- Patcher for the legacy versions: https://hack64.net/tools/patcher.php')

