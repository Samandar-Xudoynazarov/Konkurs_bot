from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database import db
from locales import _, LOCALES
from keyboards.keyboards import (
    language_keyboard, main_menu_keyboard,
    join_contest_keyboard, check_subscription_keyboard
)
from config import ADMIN_IDS
from utils import check_user_subscription, format_datetime

router = Router()


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    user = await db.get_user(message.from_user.id)

    if not user:
        # Yangi user — til tanlash
        await db.add_user(
            message.from_user.id,
            message.from_user.username or "",
            message.from_user.full_name,
            'uz'
        )
        await message.answer(
            _("uz", "choose_language"),
            reply_markup=language_keyboard()
        )
        return

    lang = user['language']
    await message.answer(
        _(lang, "start", name=message.from_user.full_name),
        reply_markup=main_menu_keyboard(lang, is_admin(message.from_user.id))
    )


@router.callback_query(F.data.startswith("lang:"))
async def callback_language(callback: CallbackQuery):
    lang = callback.data.split(":")[1]
    await db.set_user_language(callback.from_user.id, lang)

    await callback.message.delete()
    await callback.message.answer(
        _(lang, "language_changed"),
        reply_markup=main_menu_keyboard(lang, is_admin(callback.from_user.id))
    )
    await callback.answer()


@router.message(Command("help"))
async def cmd_help(message: Message):
    lang = await db.get_user_language(message.from_user.id)
    await message.answer(_(lang, "help_text"))


# ======== Tugmalar orqali ========
@router.message(lambda m: any(m.text == LOCALES[l]["change_language"] for l in LOCALES))
async def change_language(message: Message):
    await message.answer(
        _("uz", "choose_language"),
        reply_markup=language_keyboard()
    )


@router.message(lambda m: any(m.text == LOCALES[l]["help"] for l in LOCALES))
async def help_btn(message: Message):
    lang = await db.get_user_language(message.from_user.id)
    await message.answer(_(lang, "help_text"))


@router.message(lambda m: any(m.text == LOCALES[l]["main_menu"] for l in LOCALES))
async def main_menu(message: Message, state: FSMContext):
    await state.clear()
    lang = await db.get_user_language(message.from_user.id)
    await message.answer(
        _(lang, "main_menu"),
        reply_markup=main_menu_keyboard(lang, is_admin(message.from_user.id))
    )


@router.message(lambda m: any(m.text == LOCALES[l]["active_contests"] for l in LOCALES))
async def active_contests(message: Message):
    lang = await db.get_user_language(message.from_user.id)
    contests = await db.get_active_contests()

    if not contests:
        await message.answer(_(lang, "no_active_contests"))
        return

    for contest in contests:
        await send_contest_info(message, contest, lang)


async def send_contest_info(message_or_cb, contest, lang: str):
    """Konkurs haqida to'liq ma'lumot yuboradi"""
    participants_count = await db.get_participants_count(contest['id'])
    max_part = ""
    if contest['max_participants']:
        max_part = f" / {contest['max_participants']}"

    text = _(lang, "contest_info",
             title=contest['title'],
             description=contest['description'] or "—",
             prizes=contest['prizes'] or "—",
             winners_count=contest['winners_count'],
             participants=participants_count,
             max_part=max_part,
             start_date=format_datetime(contest['start_date']),
             end_date=format_datetime(contest['end_date']))

    kb = join_contest_keyboard(lang, contest['id'])

    if isinstance(message_or_cb, CallbackQuery):
        await message_or_cb.message.answer(text, reply_markup=kb, parse_mode="HTML")
    else:
        await message_or_cb.answer(text, reply_markup=kb, parse_mode="HTML")


# ======== Konkursda qatnashish ========
@router.callback_query(F.data.startswith("join:"))
async def join_contest(callback: CallbackQuery):
    contest_id = int(callback.data.split(":")[1])
    lang = await db.get_user_language(callback.from_user.id)

    contest = await db.get_contest(contest_id)
    if not contest or contest['status'] != 'active':
        await callback.answer(_(lang, "contest_not_active"), show_alert=True)
        return

    # Maksimum tekshirish
    if contest['max_participants']:
        current = await db.get_participants_count(contest_id)
        if current >= contest['max_participants']:
            await callback.answer(_(lang, "contest_full"), show_alert=True)
            return

    # Allaqachon qatnashganmi?
    if await db.is_participant(contest_id, callback.from_user.id):
        await callback.answer(_(lang, "already_joined"), show_alert=True)
        return

    # Kanallarga obunani tekshirish
    channels = await db.get_contest_channels(contest_id)
    if channels:
        all_subscribed, not_sub = await check_user_subscription(
            callback.bot, callback.from_user.id, channels
        )
        if not all_subscribed:
            channels_text = "\n".join([f"📢 {c['channel_title']}" for c in not_sub])
            await callback.message.answer(
                _(lang, "not_subscribed", channels=channels_text),
                reply_markup=check_subscription_keyboard(lang, contest_id, not_sub),
                parse_mode="HTML"
            )
            await callback.answer()
            return

    # Qatnashish
    added = await db.add_participant(contest_id, callback.from_user.id)
    if added:
        await callback.answer(_(lang, "joined_success"), show_alert=True)
        # Agar max ga yetgan bo'lsa, adminlarga xabar
        if contest['max_participants']:
            count = await db.get_participants_count(contest_id)
            if count >= contest['max_participants']:
                for admin_id in ADMIN_IDS:
                    try:
                        admin_lang = await db.get_user_language(admin_id)
                        await callback.bot.send_message(
                            admin_id,
                            _(admin_lang, "max_reached_notify", id=contest_id)
                        )
                    except Exception:
                        pass
    else:
        await callback.answer(_(lang, "already_joined"), show_alert=True)


@router.callback_query(F.data.startswith("check:"))
async def check_subscription(callback: CallbackQuery):
    contest_id = int(callback.data.split(":")[1])
    lang = await db.get_user_language(callback.from_user.id)

    contest = await db.get_contest(contest_id)
    if not contest or contest['status'] != 'active':
        await callback.answer(_(lang, "contest_not_active"), show_alert=True)
        return

    channels = await db.get_contest_channels(contest_id)
    all_subscribed, not_sub = await check_user_subscription(
        callback.bot, callback.from_user.id, channels
    )

    if not all_subscribed:
        channels_text = "\n".join([f"📢 {c['channel_title']}" for c in not_sub])
        await callback.answer(
            _(lang, "not_subscribed", channels=channels_text).split("\n\n")[0],
            show_alert=True
        )
        return

    # Obuna bo'lsa — qatnashtirish
    if await db.is_participant(contest_id, callback.from_user.id):
        await callback.answer(_(lang, "already_joined"), show_alert=True)
        return

    if contest['max_participants']:
        current = await db.get_participants_count(contest_id)
        if current >= contest['max_participants']:
            await callback.answer(_(lang, "contest_full"), show_alert=True)
            return

    await db.add_participant(contest_id, callback.from_user.id)
    await callback.message.delete()
    await callback.answer(_(lang, "joined_success"), show_alert=True)
