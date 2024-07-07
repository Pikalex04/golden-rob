

def run(bot):
    @bot.event
    async def on_message(message):
        await bot.process_commands(message)
