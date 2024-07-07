from grobDB.common import pp_leaderboard


def run(bot):
    @bot.hybrid_command(
        description='shows the Awards leaderboards', brief='Rankings',
        help='`/awards`: shows the Awards, starting from the #1\n'
             '`/awards [rank]`: shows the Awards, starting from that rank\n',
        usage='`/awards` `/awards 35`')
    async def awards(ctx):
        args = ctx.message.content.lower().split()
        start = 1
        fields = []
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
                name=f'[{score['rank']}] {score['country']} {score['name']}',
                value=f'{score['cr']}{score['points']}', inline=False)
        await pp_leaderboard(ctx, f'grobDB/ppDB/awards/awards.json', start, formatting)
