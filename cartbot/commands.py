import asyncio

import discord
from discord import app_commands

from cartbot.emoji_utils import lookup_emoji
from cartbot.model import ShoppingList
from cartbot.views import build_list_message


async def _resolve_emoji(name: str, shopping_list: ShoppingList) -> str:
    cached = shopping_list.get_emoji_for_name(name)
    if cached is not None:
        return cached
    found = await asyncio.get_running_loop().run_in_executor(None, lookup_emoji, name)
    return found or ""


def register(tree: app_commands.CommandTree, shopping_list: ShoppingList) -> None:
    @tree.command(name="add", description="Add one or more items (comma-separated) to the shopping list")
    @app_commands.describe(item="Item(s) to add, e.g. milk, bread, eggs")
    async def add_item(interaction: discord.Interaction, item: str) -> None:
        names = [part.strip() for part in item.split(",") if part.strip()]
        await interaction.response.defer()
        emojis = await asyncio.gather(*[_resolve_emoji(name, shopping_list) for name in names])
        for name, emoji in zip(names, emojis, strict=True):
            shopping_list.add(name, emoji=emoji)
        added = ", ".join(f"**{name}**" for name in names)
        await interaction.followup.send(f"Added: {added}")

    @tree.command(name="list", description="Show all items on the shopping list")
    async def list_items(interaction: discord.Interaction) -> None:
        shopping_list.remove_checked()
        items = shopping_list.get_all()
        if not items:
            await interaction.response.send_message("The shopping list is empty.")
            return
        embed, view = build_list_message(shopping_list, page=0)
        await interaction.response.send_message(embed=embed, view=view)

    @tree.command(name="help", description="Show available commands")
    async def help_command(interaction: discord.Interaction) -> None:
        await interaction.response.send_message(
            "**cartbot commands:**\n"
            "`/add <item>` - Add an item to the shopping list\n"
            "`/list` - Show all items; tick items as done one by one, next `/list` removes them\n"
            "`/help` - Show this help message"
        )
