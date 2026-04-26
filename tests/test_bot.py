from unittest.mock import AsyncMock, patch


async def test_on_ready_syncs_tree() -> None:
    with patch("cartbot.bot.tree") as mock_tree:
        mock_tree.sync = AsyncMock()
        from cartbot.bot import on_ready

        await on_ready()
        mock_tree.sync.assert_called_once()
