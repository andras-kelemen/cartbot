import discord

from cartbot.model import Item, ShoppingList

PAGE_SIZE = 25


def build_embed(items: list[Item], page: int, total_pages: int) -> discord.Embed:
    embed = discord.Embed(
        title="Shopping list",
        color=discord.Color.green() if not items else discord.Color.orange(),
    )
    embed.description = "\n".join(f"🛒 {item.name}" for item in items) or "All done! 🎉"

    footer = f"{len(items)} item(s) remaining"
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


class RemoveSelect(discord.ui.Select):
    def __init__(self, items: list[Item], page: int, shopping_list: ShoppingList) -> None:
        self._page = page
        self._shopping_list = shopping_list
        options = [discord.SelectOption(label=item.name, value=str(item.id), emoji="✅") for item in items]
        super().__init__(placeholder="Mark as purchased (removes from list)...", options=options, row=0)

    async def callback(self, interaction: discord.Interaction) -> None:
        self._shopping_list.remove(int(self.values[0]))
        embed, view = build_list_message(self._shopping_list, self._page)
        await interaction.response.edit_message(embed=embed, view=view)


class PrevButton(discord.ui.Button):
    def __init__(self, page: int, shopping_list: ShoppingList) -> None:
        super().__init__(label="◀ Prev", style=discord.ButtonStyle.secondary, row=1)
        self._page = page
        self._shopping_list = shopping_list

    async def callback(self, interaction: discord.Interaction) -> None:
        embed, view = build_list_message(self._shopping_list, self._page - 1)
        await interaction.response.edit_message(embed=embed, view=view)


class NextButton(discord.ui.Button):
    def __init__(self, page: int, shopping_list: ShoppingList) -> None:
        super().__init__(label="Next ▶", style=discord.ButtonStyle.secondary, row=1)
        self._page = page
        self._shopping_list = shopping_list

    async def callback(self, interaction: discord.Interaction) -> None:
        embed, view = build_list_message(self._shopping_list, self._page + 1)
        await interaction.response.edit_message(embed=embed, view=view)


class ShoppingListView(discord.ui.View):
    def __init__(self, items: list[Item], page: int, total_pages: int, shopping_list: ShoppingList) -> None:
        super().__init__(timeout=None)
        if items:
            self.add_item(RemoveSelect(items, page, shopping_list))
        if page > 0:
            self.add_item(PrevButton(page, shopping_list))
        if page < total_pages - 1:
            self.add_item(NextButton(page, shopping_list))
