from better_functions import better_json as bj
from grobDB.common import pp_leaderboard


categories = [['p', 'prb'], ['n', 'nonprb', 'non', 'non-prb', 'nprb']]


def run(bot):
    @bot.hybrid_command(
        description='shows the Average Rank Rating leaderboards', brief='Rankings',
        help='`/arr`: shows the ARRs, defaulting to PRB, starting from the #1\n'
             '`/arr [category]`: shows the ARRs for that category, starting from #1\n'
             '`/arr [country]`: shows the ARRs of that country, defaulting to PRB, starting from #1'
             '`/arr [rank]`: shows the ARRs, defaulting to PRB, starting from that rank\n',
        usage='`/arr` `/arr non 35` `/arr n uk` `/arr "south africa" nonprb`')
    async def arr(ctx):
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
            e.add_field(
                name=f'[{score['rank']}] {score['country']} {score['player']}',
                value=f'{score['cr']}{score['score']} - {score['change']}', inline=False)
        await pp_leaderboard(ctx, f'grobDB/ppDB/arr/{selection[1][0]}{selection[0][0]}.json', start, formatting)
