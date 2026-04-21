from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from typing import List, Tuple


async def check_user_subscription(bot: Bot, user_id: int, channels: list) -> Tuple[bool, List[dict]]:
    """
    Foydalanuvchi barcha kanallarga obuna bo'lganligini tekshiradi.
    Return: (hammasiga obunami, obuna bo'lmagan kanallar ro'yxati)
    """
    not_subscribed = []

    for ch in channels:
        try:
            member = await bot.get_chat_member(ch['channel_id'], user_id)
            # member.status: 'creator', 'administrator', 'member', 'restricted', 'left', 'kicked'
            if member.status in ('left', 'kicked'):
                not_subscribed.append(dict(ch))
        except (TelegramBadRequest, TelegramForbiddenError):
            # Agar bot kanalga kira olmasa yoki user bo'lmasa
            not_subscribed.append(dict(ch))
        except Exception:
            not_subscribed.append(dict(ch))

    return (len(not_subscribed) == 0), not_subscribed


async def resolve_channel(bot: Bot, channel_input: str) -> dict:
    """
    Kanalni aniqlaydi: @username yoki invite link orqali.
    Return: {'id': ..., 'username': ..., 'title': ..., 'link': ...}
    """
    channel_input = channel_input.strip()
    
    # Invite link holati
    if "t.me/+" in channel_input or "t.me/joinchat/" in channel_input:
        # Invite link orqali to'g'ridan-to'g'ri chat ma'lumotlarini olish qiyin
        # User @username ko'rinishida kiritishi tavsiya etiladi
        raise ValueError("Iltimos, kanalning @username ini yuboring")
    
    # URL dan username ni olish
    if "t.me/" in channel_input:
        channel_input = channel_input.split("t.me/")[-1].split("?")[0].split("/")[0]
    
    # @ belgisini olib tashlash
    username = channel_input.lstrip("@")
    
    if not username:
        raise ValueError("Noto'g'ri kanal")
    
    chat = await bot.get_chat(f"@{username}")
    
    # Botning kanalda admin ekanligini tekshirish
    bot_member = await bot.get_chat_member(chat.id, (await bot.get_me()).id)
    if bot_member.status not in ('administrator', 'creator'):
        raise ValueError("Bot kanalda admin emas")
    
    return {
        'id': chat.id,
        'username': chat.username,
        'title': chat.title,
        'link': f"https://t.me/{chat.username}" if chat.username else None,
    }
