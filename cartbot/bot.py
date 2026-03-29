import os

import discord
from discord import app_commands

from cartbot import commands
from cartbot.model import ShoppingList

intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)
shopping_list = ShoppingList(db_path=os.environ.get("DB_PATH", "cartbot.db"))

commands.register(tree, shopping_list)


@bot.event
async def on_ready() -> None:
    await tree.sync()
