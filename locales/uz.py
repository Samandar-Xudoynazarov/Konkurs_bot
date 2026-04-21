TEXTS = {
    # Umumiy
    "start": "👋 Assalomu alaykum, {name}!\n\nKonkurs botiga xush kelibsiz!",
    "choose_language": "🌐 Tilni tanlang:",
    "language_changed": "✅ Til o'zbekchaga o'zgartirildi!",
    "main_menu": "🏠 Asosiy menyu",
    "back": "◀️ Orqaga",
    "cancel": "❌ Bekor qilish",
    "cancelled": "❌ Bekor qilindi",
    "skip": "⏭ O'tkazib yuborish",
    "done": "✅ Tayyor",
    "yes": "✅ Ha",
    "no": "❌ Yo'q",

    # Foydalanuvchi menyusi
    "active_contests": "🎉 Aktiv konkurslar",
    "my_contests": "📋 Mening konkurslarim",
    "change_language": "🌐 Tilni o'zgartirish",
    "help": "ℹ️ Yordam",

    # Konkurslar ro'yxati
    "no_active_contests": "😔 Hozircha aktiv konkurslar yo'q.",
    "contest_info": (
        "🎉 <b>{title}</b>\n\n"
        "📝 {description}\n\n"
        "🎁 <b>Sovrinlar:</b>\n{prizes}\n\n"
        "🏆 <b>G'oliblar soni:</b> {winners_count}\n"
        "👥 <b>Ishtirokchilar:</b> {participants}{max_part}\n"
        "📅 <b>Boshlanish:</b> {start_date}\n"
        "📅 <b>Tugash:</b> {end_date}"
    ),
    "join_contest": "✅ Qatnashish",
    "already_joined": "✅ Siz qatnashgansiz!",
    "joined_success": "🎉 Tabriklaymiz! Siz konkursda qatnashyapsiz!",
    "not_subscribed": (
        "❌ Konkursda qatnashish uchun quyidagi kanallarga obuna bo'lishingiz shart:\n\n{channels}\n\n"
        "Obuna bo'lganingizdan keyin \"🔄 Tekshirish\" tugmasini bosing."
    ),
    "check_subscription": "🔄 Tekshirish",
    "contest_not_active": "❌ Bu konkurs hozir aktiv emas.",
    "contest_full": "❌ Konkurs ishtirokchilar sonining maksimumiga yetdi!",

    # Admin menyusi
    "admin_panel": "👑 <b>Admin panel</b>",
    "create_contest": "➕ Konkurs yaratish",
    "manage_contests": "📋 Konkurslarni boshqarish",
    "statistics": "📊 Statistika",
    "not_admin": "❌ Siz admin emassiz!",

    # Konkurs yaratish
    "enter_title": "📝 Konkurs nomini kiriting:",
    "enter_description": "📝 Konkurs tavsifini kiriting:",
    "enter_prizes": "🎁 Sovrinlarni kiriting (masalan: 1-o'rin: iPhone, 2-o'rin: AirPods):",
    "enter_winners_count": "🏆 G'oliblar sonini kiriting (masalan: 3):",
    "enter_max_participants": (
        "👥 Maksimal ishtirokchilar sonini kiriting (masalan: 1000)\n"
        "Yoki cheksiz qilish uchun \"⏭ O'tkazib yuborish\" bosing:"
    ),
    "enter_start_date": (
        "📅 Boshlanish sanasini kiriting.\n"
        "Format: YYYY-MM-DD HH:MM\n"
        "Masalan: 2026-05-01 10:00"
    ),
    "enter_end_date": (
        "📅 Tugash sanasini kiriting.\n"
        "Format: YYYY-MM-DD HH:MM\n"
        "Masalan: 2026-05-10 18:00"
    ),
    "invalid_date": "❌ Noto'g'ri sana formati! Qayta urinib ko'ring.",
    "invalid_number": "❌ Iltimos, raqam kiriting!",
    "add_channels": (
        "📢 Endi majburiy kanallarni qo'shing.\n\n"
        "Bot kanalga <b>admin</b> sifatida qo'shilgan bo'lishi kerak!\n\n"
        "Kanal @username yoki invite linkini yuboring.\n"
        "Tugatish uchun /done buyrug'ini yuboring."
    ),
    "channel_added": "✅ Kanal qo'shildi: {title}\n\nYana kanal qo'shish yoki /done bosing.",
    "channel_error": "❌ Kanalni qo'shib bo'lmadi. Bot kanalda admin ekanligiga ishonch hosil qiling.",
    "contest_created": (
        "✅ <b>Konkurs yaratildi!</b>\n\n"
        "ID: <code>{id}</code>\n"
        "Nomi: {title}\n\n"
        "Boshlash uchun \"🚀 Boshlash\" tugmasini bosing."
    ),
    "start_contest": "🚀 Konkursni boshlash",
    "contest_started": "🎉 Konkurs boshlandi! ID: {id}",
    "already_started": "⚠️ Konkurs allaqachon boshlangan!",

    # Boshqarish
    "select_contest": "📋 Konkursni tanlang:",
    "contest_status_draft": "📝 Qoralama",
    "contest_status_active": "🟢 Aktiv",
    "contest_status_finished": "🔴 Tugatilgan",
    "contest_status_cancelled": "⚫️ Bekor qilingan",
    "manage_buttons_start": "🚀 Boshlash",
    "manage_buttons_finish": "🏁 Tugatish",
    "manage_buttons_winners": "🎲 G'oliblarni aniqlash",
    "manage_buttons_participants": "👥 Ishtirokchilar",
    "manage_buttons_delete": "🗑 O'chirish",
    "confirm_delete": "⚠️ Haqiqatan o'chirmoqchimisiz?",
    "deleted": "✅ O'chirildi!",

    # G'oliblar
    "no_participants": "😔 Ishtirokchilar yo'q!",
    "winners_selected": "🎉 <b>G'oliblar aniqlandi!</b>\n\n{winners}",
    "winner_line": "{position}. {name} (@{username}) — ID: <code>{user_id}</code>",
    "winner_no_username": "{position}. {name} — ID: <code>{user_id}</code>",
    "contest_finished_notify": (
        "🏆 <b>Konkurs tugadi!</b>\n\n"
        "Konkurs: {title}\n\n"
        "G'oliblar:\n{winners}"
    ),
    "you_are_winner": (
        "🎉 <b>Tabriklaymiz! Siz {position}-o'rinni oldingiz!</b>\n\n"
        "🏆 Konkurs: {title}\n\n"
        "Mukofotingizni olish uchun admin bilan bog'laning:\n{admin_contact}"
    ),
    "you_lost": (
        "😔 Afsuski, <b>{title}</b> konkursimiz tugadi.\n\n"
        "Siz bu safar g'olib bo'la olmadingiz. Keyingi konkurslarda faolroq qatnashing va o'rinlarni oling! 💪"
    ),

    # Statistika
    "stats_text": (
        "📊 <b>Statistika</b>\n\n"
        "👥 Foydalanuvchilar: {users}\n"
        "🎉 Jami konkurslar: {contests}\n"
        "🟢 Aktiv konkurslar: {active}\n"
        "🏆 Tugatilgan: {finished}"
    ),

    # Maksimum yetdi
    "max_reached_notify": "⚠️ Konkurs {id} maksimal ishtirokchilar soniga yetdi. /winner buyrug'i bilan g'oliblarni aniqlang.",
    "winner_command_usage": "Foydalanish: /winner <contest_id>",
    "help_text": (
        "ℹ️ <b>Yordam</b>\n\n"
        "Bu bot Telegram konkurslari uchun mo'ljallangan.\n\n"
        "<b>Foydalanuvchi uchun:</b>\n"
        "• Aktiv konkurslar ro'yxatini ko'ring\n"
        "• Kanallarga obuna bo'lib qatnashing\n"
        "• G'oliblardan biri bo'ling!\n\n"
        "<b>Admin uchun:</b>\n"
        "/admin - Admin panel\n"
        "/winner <id> - G'oliblarni aniqlash"
    ),
}
