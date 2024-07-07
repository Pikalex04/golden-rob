from grobDB.common import pp_leaderboard


categories = [['w', 'pow'], ['w', 'pow'], ['q', 'poq'], ['y', 'poy']]


def run(bot):
    @bot.hybrid_command(
        description='shows the Player of a period leaderboards', brief='Rankings',
        help='`/po`: shows the POs, defaulting to POW, starting from the #1\n'
             '`/po [period]`: shows the POs for that period, starting from #1\n'
             '`/po [rank]`: shows the POs, defaulting to POW, starting from that rank\n',
        usage='`/po` `/po pow 35` `/po m 13` `/po poq` `/po y`')
    async def po(ctx):
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
                name=f'[{score['rank']}] {score['country']} {score['name']}',
                value=f'{score['cr']}{score['score']}', inline=False)
        await pp_leaderboard(ctx, f'grobDB/ppDB/po/po{selection[0][0]}.json', start, formatting)
