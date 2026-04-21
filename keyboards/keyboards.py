from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from locales import _
from config import LANGUAGES


def language_keyboard() -> InlineKeyboardMarkup:
    """Til tanlash klaviaturasi"""
    builder = InlineKeyboardBuilder()
    for code, name in LANGUAGES.items():
        builder.button(text=name, callback_data=f"lang:{code}")
    builder.adjust(1)
    return builder.as_markup()


def main_menu_keyboard(lang: str, is_admin: bool = False) -> ReplyKeyboardMarkup:
    """Asosiy menyu"""
    builder = ReplyKeyboardBuilder()
    builder.button(text=_(lang, "active_contests"))
    builder.button(text=_(lang, "change_language"))
    builder.button(text=_(lang, "help"))
    if is_admin:
        builder.button(text=_(lang, "admin_panel"))
    builder.adjust(1, 2, 1)
    return builder.as_markup(resize_keyboard=True)


def admin_panel_keyboard(lang: str) -> ReplyKeyboardMarkup:
    """Admin panel klaviaturasi"""
    builder = ReplyKeyboardBuilder()
    builder.button(text=_(lang, "create_contest"))
    builder.button(text=_(lang, "manage_contests"))
    builder.button(text=_(lang, "statistics"))
    builder.button(text=_(lang, "main_menu"))
    builder.adjust(1, 2, 1)
    return builder.as_markup(resize_keyboard=True)


def cancel_keyboard(lang: str) -> ReplyKeyboardMarkup:
    """Bekor qilish tugmasi"""
    builder = ReplyKeyboardBuilder()
    builder.button(text=_(lang, "cancel"))
    return builder.as_markup(resize_keyboard=True)


def skip_cancel_keyboard(lang: str) -> ReplyKeyboardMarkup:
    """O'tkazish + bekor qilish"""
    builder = ReplyKeyboardBuilder()
    builder.button(text=_(lang, "skip"))
    builder.button(text=_(lang, "cancel"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def join_contest_keyboard(lang: str, contest_id: int) -> InlineKeyboardMarkup:
    """Konkursda qatnashish tugmasi"""
    builder = InlineKeyboardBuilder()
    builder.button(text=_(lang, "join_contest"), callback_data=f"join:{contest_id}")
    return builder.as_markup()


def check_subscription_keyboard(lang: str, contest_id: int, channels: list) -> InlineKeyboardMarkup:
    """Obunani tekshirish klaviaturasi"""
    builder = InlineKeyboardBuilder()
    for ch in channels:
        link = ch['channel_link'] or (f"https://t.me/{ch['channel_username']}" 
                                       if ch['channel_username'] else "")
        if link:
            builder.button(text=f"📢 {ch['channel_title']}", url=link)
    builder.button(text=_(lang, "check_subscription"), callback_data=f"check:{contest_id}")
    builder.adjust(1)
    return builder.as_markup()


def contests_list_keyboard(lang: str, contests: list, prefix: str = "contest") -> InlineKeyboardMarkup:
    """Konkurslar ro'yxati"""
    builder = InlineKeyboardBuilder()
    for c in contests:
        status_emoji = {
            'draft': '📝', 'active': '🟢', 
            'finished': '🔴', 'cancelled': '⚫️'
        }.get(c['status'], '❔')
        builder.button(
            text=f"{status_emoji} #{c['id']} {c['title'][:30]}",
            callback_data=f"{prefix}:{c['id']}"
        )
    builder.adjust(1)
    return builder.as_markup()


def manage_contest_keyboard(lang: str, contest_id: int, status: str) -> InlineKeyboardMarkup:
    """Konkursni boshqarish"""
    builder = InlineKeyboardBuilder()
    if status == 'draft':
        builder.button(
            text=_(lang, "manage_buttons_start"),
            callback_data=f"cstart:{contest_id}"
        )
    if status == 'active':
        builder.button(
            text=_(lang, "manage_buttons_winners"),
            callback_data=f"cwinners:{contest_id}"
        )
        builder.button(
            text=_(lang, "manage_buttons_finish"),
            callback_data=f"cfinish:{contest_id}"
        )
    builder.button(
        text=_(lang, "manage_buttons_participants"),
        callback_data=f"cparts:{contest_id}"
    )
    if status in ('draft', 'cancelled', 'finished'):
        builder.button(
            text=_(lang, "manage_buttons_delete"),
            callback_data=f"cdelete:{contest_id}"
        )
    builder.adjust(1)
    return builder.as_markup()


def confirm_delete_keyboard(lang: str, contest_id: int) -> InlineKeyboardMarkup:
    """O'chirishni tasdiqlash"""
    builder = InlineKeyboardBuilder()
    builder.button(text=_(lang, "yes"), callback_data=f"cdel_yes:{contest_id}")
    builder.button(text=_(lang, "no"), callback_data=f"cdel_no:{contest_id}")
    builder.adjust(2)
    return builder.as_markup()
