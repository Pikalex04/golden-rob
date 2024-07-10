from discord import Embed


def run(bot):
    @bot.hybrid_command(
        description='lists all the available DNS to play online', brief='Online',
        help='`/dns`: lists the DNS', usage='`/bks`')
    async def dns(ctx):
        e = Embed(description=
                  f'{ctx.author.mention}, we highly recommend using Wiimmfi, the most active service at the moment.\n'
                  'You can see the current activity for Mario Kart DS with `/online` or by visiting the [official '
                  'website](https://wiimmfi.de/stats/game/mariokartds).\n\n'
                  'A DNS written in *italic* can be left blank.\n'
                  'A DNS written in **bold** is recommended.')
        e.set_author(name='DNS List', icon_url='https://cdn.discordapp.com/emojis/1233445494030729236.png?size=256')
        for field in [
            ['Wiimmfi', 'Primary DNS:\n`167.235.229.36`\n\n*Secondary DNS:\n**- `8.8.8.8`** or\n- `1.1.1.1`*'],
            ['WiiLink WFC', 'Primary DNS:\n`5.161.56.11`\n\n*Secondary DNS:\n**- `8.8.8.8`** or\n- `1.1.1.1`*'],
            ['Zwei.moe', 'Primary DNS:\n`172.104.88.237`\n\n*Secondary DNS:\n**- `8.8.8.8`** or\n- `1.1.1.1`*']
        ]:
            e.add_field(name=field[0], value=field[1], inline=True)
        await ctx.send(embed=e)
