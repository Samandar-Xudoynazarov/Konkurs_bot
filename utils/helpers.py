import random
from datetime import datetime
from typing import Optional


def parse_datetime(text: str) -> Optional[datetime]:
    """YYYY-MM-DD HH:MM formatidagi sanani parse qiladi"""
    formats = [
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%d.%m.%Y %H:%M",
        "%d.%m.%Y",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(text.strip(), fmt)
        except ValueError:
            continue
    return None


def format_datetime(dt) -> str:
    """Sanani chiroyli formatda qaytaradi"""
    if not dt:
        return "—"
    return dt.strftime("%Y-%m-%d %H:%M")


def select_random_winners(participants: list, count: int) -> list:
    """Random g'oliblarni tanlaydi"""
    if not participants:
        return []
    count = min(count, len(participants))
    return random.sample(participants, count)


def format_status(status: str, lang: str) -> str:
    """Statusni tilga qarab formatlaydi"""
    from locales import _
    key = f"contest_status_{status}"
    return _(lang, key)
