import discord

from cartbot.model import Item, ShoppingList

PAGE_SIZE = 20


def build_embed(items: list[Item], page: int, total_pages: int) -> discord.Embed:
    remaining = sum(1 for item in items if not item.checked)
    embed = discord.Embed(
        title="Shopping list",
        color=discord.Color.green() if not items else discord.Color.orange(),
    )
    if not items:
        embed.description = "All done! 🎉"
    footer = f"{remaining} item(s) remaining"
    if total_pages > 1:
        footer += f"  •  Page {page + 1}/{total_pages}"
    embed.set_footer(text=footer)
    return embed


def build_list_message(shopping_list: ShoppingList, page: int) -> tuple[discord.Embed, "ShoppingListView"]:
    all_items = shopping_list.get_all()
    total_pages = max(1, -(-len(all_items) // PAGE_SIZE))
    page = min(page, total_pages - 1)
    page_items = all_items[page * PAGE_SIZE : (page + 1) * PAGE_SIZE]
    return build_embed(page_items, page, total_pages), ShoppingListView(page_items, page, total_pages, shopping_list)


class ItemButton(discord.ui.Button):
    def __init__(self, item: Item, page: int, shopping_list: ShoppingList, row: int) -> None:
        style = discord.ButtonStyle.success if item.checked else discord.ButtonStyle.secondary
        emoji = "✅" if item.checked else "🛒"
        super().__init__(label=item.name, style=style, emoji=emoji, row=row)
        self._item = item
        self._page = page
        self._shopping_list = shopping_list

    async def callback(self, interaction: discord.Interaction) -> None:
        self._shopping_list.toggle_checked(self._item.id)
        embed, view = build_list_message(self._shopping_list, self._page)
        await interaction.response.edit_message(embed=embed, view=view)


class NavButton(discord.ui.Button):
    def __init__(self, label: str, page: int, offset: int, shopping_list: ShoppingList) -> None:
        super().__init__(label=label, style=discord.ButtonStyle.secondary, row=4)
        self._page = page
        self._offset = offset
        self._shopping_list = shopping_list

    async def callback(self, interaction: discord.Interaction) -> None:
        embed, view = build_list_message(self._shopping_list, self._page + self._offset)
        await interaction.response.edit_message(embed=embed, view=view)


class ShoppingListView(discord.ui.View):
    def __init__(self, items: list[Item], page: int, total_pages: int, shopping_list: ShoppingList) -> None:
        super().__init__(timeout=None)
        for i, item in enumerate(items):
            self.add_item(ItemButton(item, page, shopping_list, row=i // 5))
        if page > 0:
            self.add_item(NavButton("◀ Prev", page, -1, shopping_list))
        if page < total_pages - 1:
            self.add_item(NavButton("Next ▶", page, +1, shopping_list))
