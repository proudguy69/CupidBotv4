from discord.ext.commands import Bot
from discord import Intents

class Cupidv4(Bot):
    def __init__(self):
        super().__init__(command_prefix='?', intents=Intents.all())


def main():
    bot = Cupidv4()
    bot.run()

if __name__ == "__main__":
    main()