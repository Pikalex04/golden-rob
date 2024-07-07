from better_functions import better_json as bj
from grobDB.common import pp_leaderboard


categories = [['p', 'prb'], ['n', 'nonprb', 'non', 'non-prb', 'nprb']]
tracks = [
    ['f8c'], ['yf'], ['ccb'], ['lm'], ['dh'], ['ds'], ['wp'], ['sr'], ['dkp'], ['ttc'], ['mc'], ['af'], ['ws'], ['pg'],
    ['bc'], ['rr'], ['rmc1', 'mc1', 'rmc'], ['rmmf', 'mmf'], ['rpc', 'pc'], ['rlc1', 'lc1'],
    ['rdp1', 'rdp', 'dp', 'dp1'], ['rfs', 'fs'], ['rbc2', 'bc2', 'rbc'], ['rbp', 'bp'], ['rkb2', 'kb2', 'rkb'],
    ['rcm', 'cm'], ['rlc2', 'lc2'], ['rci2', 'ci2', 'rci', 'ci'], ['rbb', 'bb'], ['rsg', 'sg'], ['ryc', 'yc']]
laps = [['3lap', 'course', 'full', '5lap'], ['flap', 'lap', '1lap', 'best']]


def run(bot):
    @bot.hybrid_command(
        description='shows the Standards of a track', brief='Rankings', aliases=['std', 'standard'],
        help='`/standards`: shows the times, defaulting the chart to PRB Figure-8 Circuit Course, starting from the '
             '#1\n'
             '`/standards [category]`: shows the times for that category, defaulting to Figure-8 Circuit Course, '
             'starting from #1\n'
             '`/standards [track]`: shows the times for that track, defaulting to PRB Course, starting from #1\n'
             '`/standards [laps]`: shows the times for those laps, defaulting to PRB Figure-8 Circuit, starting from '
             '#1\n',
        usage='`/standards` `/standards n yf flap` `/standards mmf non 1lap` `/standards lap nonprb rmc` '
              '`/standards nprb 3lap rkb2` `standards p 3lap rr`')
    async def standards(ctx):
        args = ctx.message.content.lower().split()
        start = 1
        countries = bj.json_load('grobDB/ppDB/countries.json')
        fields = [categories, tracks, laps, countries]
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
                name=f'{score['std']} ({score['time']})', value=f'{score['amount']} players ({score['percentage']}%)',
                inline=False)
        await pp_leaderboard(
            ctx, f'grobDB/ppDB/standards/{selection[3][0]}{selection[0][0]}'
                 f'{tracks.index(selection[1]) * 2 + laps.index(selection[2])}.json', start, formatting)
