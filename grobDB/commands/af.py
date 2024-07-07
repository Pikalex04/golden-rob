from better_functions import better_json as bj
from grobDB.common import pp_leaderboard


categories = [['p', 'prb'], ['n', 'nonprb', 'non', 'non-prb', 'nprb']]


def run(bot):
    @bot.hybrid_command(
        description='shows the Average Finish leaderboards', brief='Rankings',
        help='`/af`: shows the AFs, defaulting to PRB, starting from the #1\n'
             '`/af [category]`: shows the AFs for that category, starting from #1\n'
             '`/af [country]`: shows the AFs of that country, defaulting to PRB, starting from #1'
             '`/af [rank]`: shows the AFs, defaulting to PRB, starting from that rank\n',
        usage='`/af` `/af non 35` `/af n "south korea"` `/af "new zealand" nonprb`')
    async def af(ctx):
        args = ctx.message.content.lower().split()
        start = 1
        countries = bj.json_load('grobDB/ppDB/countries.json')
        fields = [categories, countries]
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
            try:
                e.add_field(
                    name=f'[{score['rank']}] {score['country']} {score['player']}',
                    value=f'{score['cr']}{score['score']} - {score['change']}', inline=False)
            except KeyError:
                e.add_field(
                    name=f'[{score['rank']}] {score['country']} {score['player']}',
                    value=f'{score['score']}', inline=False)
        await pp_leaderboard(ctx, f'grobDB/ppDB/af/{selection[1][0]}{selection[0][0]}.json', start, formatting)
