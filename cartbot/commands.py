import discord
from discord import app_commands

from cartbot.model import ShoppingList
from cartbot.views import build_list_message


def register(tree: app_commands.CommandTree, shopping_list: ShoppingList) -> None:
    @tree.command(name="add", description="Add one or more items (comma-separated) to the shopping list")
    @app_commands.describe(item="Item(s) to add, e.g. milk, bread, eggs")
    async def add_item(interaction: discord.Interaction, item: str) -> None:
        items = [part.strip() for part in item.split(",") if part.strip()]
        for i in items:
            shopping_list.add(i)
        added = ", ".join(f"**{i}**" for i in items)
        await interaction.response.send_message(f"Added: {added}")

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
