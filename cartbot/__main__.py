import os

from cartbot.bot import bot

token = os.environ["DISCORD_TOKEN"]
bot.run(token)
