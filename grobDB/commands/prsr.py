from better_functions import better_json as bj
from grobDB.common import pp_leaderboard


categories = [['p', 'prb'], ['n', 'nonprb', 'non', 'non-prb', 'nprb']]


def run(bot):
    @bot.hybrid_command(
        description='shows the Personal Record : Site Record leaderboards', brief='Rankings',
        help='`/prsr`: shows the PRSRs, defaulting to PRB, starting from the #1\n'
             '`/prsr [category]`: shows the ARRs for that category, starting from #1\n'
             '`/prsr [country]`: shows the ARRs of that country, defaulting to PRB, starting from #1'
             '`/prsr [rank]`: shows the ARRs, defaulting to PRB, starting from that rank\n',
        usage='`/prsr` `/prsr non 35` `/prsr n japan` `/prsr "north macedonia" nonprb`')
    async def prsr(ctx):
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
        await pp_leaderboard(ctx, f'grobDB/ppDB/prsr/{selection[1][0]}{selection[0][0]}.json', start, formatting)
