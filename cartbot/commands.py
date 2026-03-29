import discord
from discord import app_commands

from cartbot.model import ShoppingList
from cartbot.views import build_list_message


def register(tree: app_commands.CommandTree, shopping_list: ShoppingList) -> None:
    @tree.command(name="add", description="Add an item to the shopping list")
    @app_commands.describe(item="The item to add")
    async def add_item(interaction: discord.Interaction, item: str) -> None:
        shopping_list.add(item)
        await interaction.response.send_message(f"Added: **{item.strip()}**")

    @tree.command(name="list", description="Show all items on the shopping list")
    async def list_items(interaction: discord.Interaction) -> None:
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
            "`/list` - Show all items; select one to mark it as purchased and remove it\n"
            "`/help` - Show this help message"
        )
