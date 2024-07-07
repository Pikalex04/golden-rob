from grobDB.common import pp_leaderboard


categories = [['p', 'prb'], ['n', 'nonprb', 'non', 'non-prb', 'nprb']]
laps = [
    [0, 'champion', 'champ', 'cha'], [2, 'cumulative', 'days', 'individual', 'cum', 'd'],
    [1, 'countries', 'country', 'cou']]


def run(bot):
    @bot.hybrid_command(
        description='shows the Former #1 leaderboards', brief='Rankings', aliases=['former_1'],
        help='`/former1`: shows the F#1s, defaulting the chart to PRB Champions, starting from the #1\n'
             '`/former1 [category]`: shows the F#1s for that category, defaulting to Champions, starting from #1\n'
             '`/former1 [ranking]`: shows the F#1s for that ranking (champions, cumulative or countries), defaulting '
             'to PRB, starting from #1\n'
             '`/former1 [rank]`: shows the F#1s, defaulting to PRB Champions, starting from that rank\n',
        usage='`/former1` `/former1 non 30` `/former1 cumulative non 5` `/former1 597 days nonprb` '
              '`/former1 country`')
    async def former1(ctx):
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
            if 0 == selection[1][0]:
                e.add_field(
                    name=f'{score['country']} {score['name']}',
                    value=f'{score['range']} ({score['duration']}, {score['percentage']})', inline=False)
            elif 2 == selection[1][0]:
                e.add_field(
                    name=f'[{score['rank']}] {score['country']} {score['player']}',
                    value=f'{score['cr']}{score['duration']} days ({score['total']})', inline=False)
            else:
                e.add_field(
                    name=f'[{score['rank']}] {score['country']} {score['og_country']}',
                    value=f'{score['duration']} days ({score['total']})', inline=False)
        await pp_leaderboard(
            ctx, f'grobDB/ppDB/former1/{selection[0][0]}{selection[1][0]}.json', start,
            formatting)
