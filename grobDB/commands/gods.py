from grobDB.common import pp_leaderboard


categories = [['p', 'prb'], ['n', 'nonprb', 'non', 'non-prb', 'nprb']]


def run(bot):
    @bot.hybrid_command(
        description='shows the Gods leaderboards', brief='Rankings', aliases=['god'],
        help='`/gods`: shows the Gods, defaulting the chart to PRB, starting from the #1\n'
             '`/gods [category]`: shows the Gods for that category, starting from #1\n'
             '`/gods [rank]`: shows the Gods, defaulting to PRB, starting from that rank\n',
        usage='`/gods` `/gods non 30`')
    async def gods(ctx):
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
                name=f'[{score['rank']}] {score['country']} {score['player']}',
                value=f'{score['count']}/64 Gods', inline=False)
        await pp_leaderboard(ctx, f'grobDB/ppDB/gods/{selection[0][0]}.json', start, formatting)
