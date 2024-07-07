from better_functions import better_json as bj
from grobDB.common import pp_leaderboard


categories = [['p', 'prb'], ['n', 'nonprb', 'non', 'non-prb', 'nprb']]
tracks = [
    ['f8c'], ['yf'], ['ccb'], ['lm'], ['dh'], ['ds'], ['wp'], ['sr'], ['dkp'], ['ttc'], ['mc'], ['af'], ['ws'], ['pg'],
    ['bc'], ['rr'], ['rmc1', 'mc1', 'rmc'], ['rmmf', 'mmf'], ['rpc', 'pc'], ['rlc1', 'lc1'],
    ['rdp1', 'rdp', 'dp', 'dp1'], ['rfs', 'fs'], ['rbc2', 'bc2', 'rbc'], ['rbp', 'bp'], ['rkb2', 'kb2', 'rkb'],
    ['rcm', 'cm'], ['rlc2', 'lc2'], ['rmb', 'mb'], ['rci2', 'ci2', 'rci', 'ci'], ['rbb', 'bb'], ['rsg', 'sg'],
    ['ryc', 'yc']]
laps = [['3lap', 'course', 'full', '5lap'], ['flap', 'lap', '1lap', 'best']]


def run(bot):
    @bot.hybrid_command(
        description='shows the Time Trials leaderboards of a track', brief='Rankings',
        help='`/times`: shows the times, defaulting the chart to PRB Figure-8 Circuit Course, starting from the #1\n'
             '`/times [category]`: shows the times for that category, defaulting to Figure-8 Circuit Course, starting '
             'from #1\n'
             '`/times [track]`: shows the times for that track, defaulting to PRB Course, starting from #1\n'
             '`/times [laps]`: shows the times for those laps, defaulting to PRB Figure-8 Circuit, starting from #1\n'
             '`/times [country]`: shows the times of that country, defaulting to PRB Figure-8 Circuit Course, '
             'starting from #1\n'
             '`/times [rank]`: shows the times, defaulting to PRB Figure-8 Circuit Course, starting from that rank\n',
        usage='`/times` `/times n yf flap 253 usa` `/times mmf non 1lap italy 30` `/times 597 lap nonprb rmc` '
              '`/times nprb "el salvador" 3lap rkb2` `times p "hong kong" 3lap rr`')
    async def times(ctx):
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
            try:
                e.add_field(
                    name=f'[{score['rank']}] {score['country']} {score['player']}',
                    value=f'{score['cr']}'
                          f'{f'[{score['time']}]({score['video']})' if score['video'] != '' else score['time']} '
                          f'({score['std']}) - {score['date']}', inline=False)
            except KeyError:
                e.add_field(
                    name=f'[{score['rank']}] {score['country']} {score['player']}',
                    value=f'{f'[{score['time']}]({score['video']})' if score['video'] != '' else score['time']} '
                          f'({score['std']}) - {score['date']}', inline=False)
        await pp_leaderboard(
            ctx, f'grobDB/ppDB/times/{selection[3][0]}{selection[0][0]}'
                 f'{tracks.index(selection[1]) * 2 + laps.index(selection[2])}.json', start, formatting)

