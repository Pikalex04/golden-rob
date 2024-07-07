from grobDB.common import pp_leaderboard


categories = [['p', 'prb'], ['n', 'nonprb', 'non', 'non-prb', 'nprb']]
laps = [['c', '3lap', 'course', 'full', '5lap'], ['l', 'flap', 'lap', '1lap', 'best'], ['a', 'combined', 'comb']]


def run(bot):
    @bot.hybrid_command(
        description='shows the Totals leaderboards', brief='Rankings', aliases=['total'],
        help='`/totals`: shows the totals, defaulting the chart to PRB Course, starting from the #1\n'
             '`/totals [category]`: shows the totals for that category, defaulting to Course, starting from #1\n'
             '`/totals [laps]`: shows the totals for those laps, defaulting to PRB, starting from #1\n'
             '`/totals [rank]`: shows the totals, defaulting to PRB Course, starting from that rank\n',
        usage='`/totals` `/totals non 30` `/totals lap non 74` `/totals 597 comb nonprb` '
              '`/totals a` `/totals comb`')
    async def totals(ctx):
        args = ctx.message.content.lower().split()
        start = 1
        fields = [categories, laps]
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
                name=f'[{score['rank']}] {score['country']} {score['player']}',
                value=f'{score['cr']}{score['score']}', inline=False)
        await pp_leaderboard(
            ctx, f'grobDB/ppDB/totals/{selection[0][0]}{selection[1][0]}.json', start, formatting)
