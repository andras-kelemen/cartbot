import os

import emoji as emoji_lib
from deep_translator import GoogleTranslator

_SOURCE_LANG = os.environ.get("TRANSLATE_SOURCE_LANG", "hu")


def _matches(needle: str, en_name: str, aliases: list[str]) -> bool:
    return needle in en_name or any(needle in a for a in aliases)


def _search_emoji(word: str) -> str | None:
    needle = word.lower().replace(" ", "_")
    for char, data in emoji_lib.EMOJI_DATA.items():
        en_name = data.get("en", "").strip(":").lower()
        aliases = [a.strip(":").lower() for a in data.get("alias", [])]
        if _matches(needle, en_name, aliases):
            return char
        if any(_matches(part, en_name, aliases) for part in needle.split("_") if len(part) > 3):
            return char
    return None


def lookup_emoji(word: str) -> str | None:
    try:
        english = GoogleTranslator(source=_SOURCE_LANG, target="en").translate(word)
        return _search_emoji(english)
    except Exception:
        return None
