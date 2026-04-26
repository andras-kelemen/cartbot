from unittest.mock import patch

from cartbot.emoji_utils import _search_emoji, lookup_emoji


def test_search_emoji_exact_match() -> None:
    assert _search_emoji("pizza") == "🍕"


def test_search_emoji_finds_via_alias() -> None:
    result = _search_emoji("apple")
    assert result is not None


def test_search_emoji_finds_via_substring() -> None:
    # "milk" is a substring of "glass_of_milk"
    assert _search_emoji("milk") == "🥛"


def test_search_emoji_finds_via_word_part() -> None:
    # "xfake_croissant" doesn't match any full CLDR name, but the "croissant" part does
    assert _search_emoji("xfake croissant") is not None


def test_search_emoji_returns_none_for_unknown_word() -> None:
    assert _search_emoji("xyzzyx") is None


def test_lookup_emoji_returns_emoji_for_translated_word() -> None:
    with patch("cartbot.emoji_utils.GoogleTranslator") as mock_cls:
        mock_cls.return_value.translate.return_value = "pizza"
        result = lookup_emoji("pizza")
    assert result == "🍕"


def test_lookup_emoji_returns_none_on_translator_exception() -> None:
    with patch("cartbot.emoji_utils.GoogleTranslator") as mock_cls:
        mock_cls.return_value.translate.side_effect = Exception("network error")
        result = lookup_emoji("something")
    assert result is None


def test_lookup_emoji_returns_none_when_no_emoji_found() -> None:
    with patch("cartbot.emoji_utils.GoogleTranslator") as mock_cls:
        mock_cls.return_value.translate.return_value = "xyzzyx"
        result = lookup_emoji("xyzzyx")
    assert result is None
