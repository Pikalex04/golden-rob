from grobDB.common import pp_leaderboard


categories = [['p', 'prb'], ['n', 'nonprb', 'non', 'non-prb', 'nprb']]
laps = [
    [3, 'top3', 'top 3', 't3'], [2, 'top2', 'top 2', 't2'], [1, 'top1', 'top 1', 't1'],
    ['all', 'every', 'every score', 'score', 'all scores', 'e', 'a']]


def run(bot):
    @bot.hybrid_command(
        description='shows the Country AF leaderboards', brief='Rankings', aliases=['countryaf'],
        help='`/country_af`: shows the Country AFs, defaulting the chart to PRB Top 3, starting from the #1\n'
             '`/country_af [category]`: shows the Country AFs for that category, defaulting to Top 3, starting from '
             '#1\n'
             '`/country_af [top]`: shows the Country AFs for that top, defaulting to PRB, starting from #1\n'
             '`/country_af [country]`: shows the Country AFs of that country, defaulting to PRB Top 3, starting from '
             '#1\n'
             '`/country_af [rank]`: shows the Country AFs, defaulting to PRB Top 3, starting from that rank\n',
        usage='`/country_af` `/country_af non 30` `/country_af top1 non 74` `/country_af 597 t2 nonprb` '
              '`/country_af every` `/country_af e`')
    async def country_af(ctx):
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
                name=f'[{score['rank']}] {score['flag']} {score['country']}',
                value=f'{score['score']} ({score['participation']}/64)', inline=False)
        await pp_leaderboard(
            ctx, f'grobDB/ppDB/countryaf/{selection[0][0]}{selection[1][0]}.json', start,
            formatting)
