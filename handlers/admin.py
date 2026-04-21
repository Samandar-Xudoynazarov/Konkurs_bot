from aiogram import Router, F
from aiogram.utils.text_decorations import html_decoration as hd
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from database import db
from locales import _, LOCALES
from keyboards.keyboards import (
    admin_panel_keyboard, main_menu_keyboard, cancel_keyboard,
    skip_cancel_keyboard, contests_list_keyboard,
    manage_contest_keyboard, confirm_delete_keyboard
)
from config import ADMIN_IDS
from states import CreateContest
from utils import parse_datetime, format_datetime, select_random_winners, resolve_channel

router = Router()


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


# ========== Admin panel ==========
@router.message(Command("admin"))
async def cmd_admin(message: Message):
    lang = await db.get_user_language(message.from_user.id)
    if not is_admin(message.from_user.id):
        await message.answer(_(lang, "not_admin"))
        return
    await message.answer(
        _(lang, "admin_panel"),
        reply_markup=admin_panel_keyboard(lang),
        parse_mode="HTML"
    )


@router.message(lambda m: is_admin(m.from_user.id) and any(
    m.text == LOCALES[l]["admin_panel"] for l in LOCALES))
async def admin_panel_btn(message: Message):
    lang = await db.get_user_language(message.from_user.id)
    await message.answer(
        _(lang, "admin_panel"),
        reply_markup=admin_panel_keyboard(lang),
        parse_mode="HTML"
    )


# ========== Konkurs yaratish (FSM) ==========
@router.message(lambda m: is_admin(m.from_user.id) and any(
    m.text == LOCALES[l]["create_contest"] for l in LOCALES))
async def start_create_contest(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    await state.set_state(CreateContest.title)
    await message.answer(_(lang, "enter_title"), reply_markup=cancel_keyboard(lang))


@router.message(F.text.in_([LOCALES[l]["cancel"] for l in LOCALES]))
async def cancel_any(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    lang = await db.get_user_language(message.from_user.id)
    await message.answer(
        _(lang, "cancelled"),
        reply_markup=admin_panel_keyboard(lang) if is_admin(message.from_user.id) 
                     else main_menu_keyboard(lang, False)
    )


@router.message(CreateContest.title)
async def contest_title(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    await state.update_data(title=message.text)
    await state.set_state(CreateContest.description)
    await message.answer(_(lang, "enter_description"), reply_markup=cancel_keyboard(lang))


@router.message(CreateContest.description)
async def contest_description(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    await state.update_data(description=message.text)
    await state.set_state(CreateContest.prizes)
    await message.answer(_(lang, "enter_prizes"), reply_markup=cancel_keyboard(lang))


@router.message(CreateContest.prizes)
async def contest_prizes(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    await state.update_data(prizes=message.text)
    await state.set_state(CreateContest.winners_count)
    await message.answer(_(lang, "enter_winners_count"), reply_markup=cancel_keyboard(lang))


@router.message(CreateContest.winners_count)
async def contest_winners_count(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    if not message.text.isdigit() or int(message.text) < 1:
        await message.answer(_(lang, "invalid_number"))
        return
    await state.update_data(winners_count=int(message.text))
    await state.set_state(CreateContest.max_participants)
    await message.answer(
        _(lang, "enter_max_participants"),
        reply_markup=skip_cancel_keyboard(lang)
    )


@router.message(CreateContest.max_participants)
async def contest_max_participants(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    text = message.text.strip()

    # Skip tekshirish
    if text in [LOCALES[l]["skip"] for l in LOCALES]:
        await state.update_data(max_participants=None)
    elif text.isdigit() and int(text) > 0:
        await state.update_data(max_participants=int(text))
    else:
        await message.answer(_(lang, "invalid_number"))
        return

    await state.set_state(CreateContest.start_date)
    await message.answer(_(lang, "enter_start_date"), reply_markup=cancel_keyboard(lang))


@router.message(CreateContest.start_date)
async def contest_start_date(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    dt = parse_datetime(message.text)
    if not dt:
        await message.answer(_(lang, "invalid_date"))
        return
    await state.update_data(start_date=dt)
    await state.set_state(CreateContest.end_date)
    await message.answer(_(lang, "enter_end_date"), reply_markup=cancel_keyboard(lang))


@router.message(CreateContest.end_date)
async def contest_end_date(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    dt = parse_datetime(message.text)
    if not dt:
        await message.answer(_(lang, "invalid_date"))
        return
    await state.update_data(end_date=dt, channels=[])
    await state.set_state(CreateContest.channels)
    await message.answer(
        _(lang, "add_channels"),
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML"
    )


@router.message(CreateContest.channels, Command("done"))
async def contest_channels_done(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    data = await state.get_data()

    # Konkursni yaratish
    contest_id = await db.create_contest(
        title=data['title'],
        description=data['description'],
        prizes=data['prizes'],
        winners_count=data['winners_count'],
        max_participants=data.get('max_participants'),
        start_date=data['start_date'],
        end_date=data['end_date'],
        created_by=message.from_user.id,
    )

    # Kanallarni qo'shish
    for ch in data.get('channels', []):
        await db.add_channel(
            contest_id, ch['id'], ch['username'], ch['title'], ch['link']
        )

    await state.clear()
    await message.answer(
        _(lang, "contest_created", id=contest_id, title=data['title']),
        reply_markup=admin_panel_keyboard(lang),
        parse_mode="HTML"
    )


@router.message(CreateContest.channels)
async def contest_add_channel(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    try:
        ch = await resolve_channel(message.bot, message.text)
        data = await state.get_data()
        channels = data.get('channels', [])
        # Takror emasmi?
        if not any(c['id'] == ch['id'] for c in channels):
            channels.append(ch)
        await state.update_data(channels=channels)
        await message.answer(_(lang, "channel_added", title=ch['title']))
    except Exception as e:
        await message.answer(f"{_(lang, 'channel_error')}\n\n<i>{hd.quote(str(e))}</i>", parse_mode="HTML")


# ========== Konkurslarni boshqarish ==========
@router.message(lambda m: is_admin(m.from_user.id) and any(
    m.text == LOCALES[l]["manage_contests"] for l in LOCALES))
async def manage_contests(message: Message):
    lang = await db.get_user_language(message.from_user.id)
    contests = await db.get_all_contests()
    if not contests:
        await message.answer(_(lang, "no_active_contests"))
        return
    await message.answer(
        _(lang, "select_contest"),
        reply_markup=contests_list_keyboard(lang, contests, prefix="mc")
    )


@router.callback_query(F.data.startswith("mc:"))
async def manage_contest_detail(callback: CallbackQuery):
    contest_id = int(callback.data.split(":")[1])
    lang = await db.get_user_language(callback.from_user.id)
    contest = await db.get_contest(contest_id)
    if not contest:
        await callback.answer("Not found", show_alert=True)
        return

    participants = await db.get_participants_count(contest_id)
    max_part = f" / {contest['max_participants']}" if contest['max_participants'] else ""

    from utils import format_status
    text = (
        f"<b>#{contest['id']} — {contest['title']}</b>\n\n"
        f"📝 {contest['description'] or '—'}\n\n"
        f"🎁 <b>{contest['prizes'] or '—'}</b>\n\n"
        f"🏆 G'oliblar: {contest['winners_count']}\n"
        f"👥 Ishtirokchilar: {participants}{max_part}\n"
        f"📅 {format_datetime(contest['start_date'])} → {format_datetime(contest['end_date'])}\n"
        f"📊 {format_status(contest['status'], lang)}"
    )

    await callback.message.edit_text(
        text,
        reply_markup=manage_contest_keyboard(lang, contest_id, contest['status']),
        parse_mode="HTML"
    )
    await callback.answer()


# ========== Konkursni boshlash ==========
@router.callback_query(F.data.startswith("cstart:"))
async def start_contest_cb(callback: CallbackQuery):
    contest_id = int(callback.data.split(":")[1])
    lang = await db.get_user_language(callback.from_user.id)
    contest = await db.get_contest(contest_id)
    if not contest:
        await callback.answer("Not found", show_alert=True)
        return
    if contest['status'] != 'draft':
        await callback.answer(_(lang, "already_started"), show_alert=True)
        return
    await db.update_contest_status(contest_id, 'active')
    await callback.answer(_(lang, "contest_started", id=contest_id), show_alert=True)
    await manage_contest_detail(callback)


# ========== Tugatish ==========
@router.callback_query(F.data.startswith("cfinish:"))
async def finish_contest_cb(callback: CallbackQuery):
    contest_id = int(callback.data.split(":")[1])
    await db.update_contest_status(contest_id, 'finished')
    await callback.answer("✅", show_alert=False)
    await manage_contest_detail(callback)


# ========== G'oliblarni aniqlash ==========
@router.callback_query(F.data.startswith("cwinners:"))
async def pick_winners_cb(callback: CallbackQuery):
    contest_id = int(callback.data.split(":")[1])
    await pick_and_announce_winners(callback.bot, contest_id, callback.from_user.id)
    await callback.answer("✅")


async def pick_and_announce_winners(bot, contest_id: int, admin_id: int):
    """G'oliblarni tanlab e'lon qiladi"""
    lang = await db.get_user_language(admin_id)
    contest = await db.get_contest(contest_id)
    if not contest:
        return

    participants = await db.get_participants(contest_id)
    if not participants:
        await bot.send_message(admin_id, _(lang, "no_participants"))
        return

    winners = select_random_winners(participants, contest['winners_count'])

    # Eski g'oliblarni tozalash (agar qayta aniqlansa)
    await db.clear_winners(contest_id)

    winner_lines = []
    for i, user_id in enumerate(winners, start=1):
        await db.add_winner(contest_id, user_id, i)
        user = await db.get_user(user_id)
        if user and user['username']:
            line = _(lang, "winner_line",
                     position=i, name=user['full_name'] or "—",
                     username=user['username'], user_id=user_id)
        else:
            line = _(lang, "winner_no_username",
                     position=i,
                     name=(user['full_name'] if user else "—"),
                     user_id=user_id)
        winner_lines.append(line)

    winners_text = "\n".join(winner_lines)

    # Adminga xabar
    await bot.send_message(
        admin_id,
        _(lang, "winners_selected", winners=winners_text),
        parse_mode="HTML"
    )

    # Statusni 'finished' qilamiz
    await db.update_contest_status(contest_id, 'finished')

    # Admin kontakt linkini tayyorlash
    admin_user = await db.get_user(admin_id)
    if admin_user and admin_user['username']:
        admin_contact = f"<a href='https://t.me/{admin_user['username']}'>@{admin_user['username']}</a>"
    else:
        admin_contact = f"<a href='tg://user?id={admin_id}'>Admin</a>"

    # Har bir g'olibga o'z o'rni bilan xabar
    winner_set = set(winners)
    for i, user_id in enumerate(winners, start=1):
        try:
            user_lang = await db.get_user_language(user_id)
            await bot.send_message(
                user_id,
                _(user_lang, "you_are_winner",
                  position=i,
                  title=contest['title'],
                  admin_contact=admin_contact),
                parse_mode="HTML"
            )
        except Exception:
            pass

    # Yutqazganlarga tasalli xabari
    all_participants = await db.get_participants(contest_id)
    for user_id in all_participants:
        if user_id in winner_set:
            continue
        try:
            user_lang = await db.get_user_language(user_id)
            await bot.send_message(
                user_id,
                _(user_lang, "you_lost", title=contest['title']),
                parse_mode="HTML"
            )
        except Exception:
            pass


# ========== /winner buyrug'i ==========
@router.message(Command("winner"))
async def cmd_winner(message: Message):
    lang = await db.get_user_language(message.from_user.id)
    if not is_admin(message.from_user.id):
        await message.answer(_(lang, "not_admin"))
        return

    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        await message.answer(_(lang, "winner_command_usage"))
        return

    contest_id = int(args[1])
    await pick_and_announce_winners(message.bot, contest_id, message.from_user.id)


# ========== Ishtirokchilar ==========
@router.callback_query(F.data.startswith("cparts:"))
async def show_participants(callback: CallbackQuery):
    contest_id = int(callback.data.split(":")[1])
    count = await db.get_participants_count(contest_id)
    await callback.answer(f"👥 Ishtirokchilar: {count}", show_alert=True)


# ========== O'chirish ==========
@router.callback_query(F.data.startswith("cdelete:"))
async def confirm_delete(callback: CallbackQuery):
    contest_id = int(callback.data.split(":")[1])
    lang = await db.get_user_language(callback.from_user.id)
    await callback.message.edit_text(
        _(lang, "confirm_delete"),
        reply_markup=confirm_delete_keyboard(lang, contest_id)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("cdel_yes:"))
async def delete_yes(callback: CallbackQuery):
    contest_id = int(callback.data.split(":")[1])
    lang = await db.get_user_language(callback.from_user.id)
    await db.delete_contest(contest_id)
    await callback.message.edit_text(_(lang, "deleted"))
    await callback.answer()


@router.callback_query(F.data.startswith("cdel_no:"))
async def delete_no(callback: CallbackQuery):
    await manage_contest_detail(callback)


# ========== Statistika ==========
@router.message(lambda m: is_admin(m.from_user.id) and any(
    m.text == LOCALES[l]["statistics"] for l in LOCALES))
async def show_stats(message: Message):
    lang = await db.get_user_language(message.from_user.id)

    async with db.pool.acquire() as conn:
        users = await conn.fetchval("SELECT COUNT(*) FROM users")
        total = await conn.fetchval("SELECT COUNT(*) FROM contests")
        active = await conn.fetchval("SELECT COUNT(*) FROM contests WHERE status='active'")
        finished = await conn.fetchval("SELECT COUNT(*) FROM contests WHERE status='finished'")

    await message.answer(
        _(lang, "stats_text",
          users=users, contests=total, active=active, finished=finished),
        parse_mode="HTML"
    )
