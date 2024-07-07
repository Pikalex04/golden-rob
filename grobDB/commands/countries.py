from grobDB.common import pp_leaderboard


categories = [['p', 'prb'], ['n', 'nonprb', 'non', 'non-prb', 'nprb']]


def run(bot):
    @bot.hybrid_command(
        description='shows the Countries leaderboards', brief='Rankings', aliases=['country'],
        help='`/countries`: shows the Countries, defaulting the chart to PRB, starting from the #1\n'
             '`/countries [category]`: shows the Countries for that category, starting from #1\n'
             '`/countries [rank]`: shows the Countries, defaulting to PRB, starting from that rank\n',
        usage='`/countries` `/countries non 30`')
    async def countries(ctx):
        args = ctx.message.content.lower().split()
        start = 1
        fields = [categories]
        selection = []
        for field in fields:
            selection.append(field[0])
        for arg in args:
            for field in fields:
                for values in field:
                    if arg in values:
                        selection[fields.index(field)] = values
                        break
            if arg.isdigit():
                start = arg

        def formatting(e, score):
            e.add_field(
                name=f'[{score['rank']}] {score['flag']} {score['country']}',
                value=f'{score['amount']} players ({score['percentage']})', inline=False)
        await pp_leaderboard(ctx, f'grobDB/ppDB/countries/{selection[0][0]}.json', start, formatting)
