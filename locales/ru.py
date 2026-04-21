TEXTS = {
    "start": "👋 Здравствуйте, {name}!\n\nДобро пожаловать в бот конкурсов!",
    "choose_language": "🌐 Выберите язык:",
    "language_changed": "✅ Язык изменён на русский!",
    "main_menu": "🏠 Главное меню",
    "back": "◀️ Назад",
    "cancel": "❌ Отмена",
    "cancelled": "❌ Отменено",
    "skip": "⏭ Пропустить",
    "done": "✅ Готово",
    "yes": "✅ Да",
    "no": "❌ Нет",

    "active_contests": "🎉 Активные конкурсы",
    "my_contests": "📋 Мои конкурсы",
    "change_language": "🌐 Сменить язык",
    "help": "ℹ️ Помощь",

    "no_active_contests": "😔 Пока нет активных конкурсов.",
    "contest_info": (
        "🎉 <b>{title}</b>\n\n"
        "📝 {description}\n\n"
        "🎁 <b>Призы:</b>\n{prizes}\n\n"
        "🏆 <b>Количество победителей:</b> {winners_count}\n"
        "👥 <b>Участники:</b> {participants}{max_part}\n"
        "📅 <b>Начало:</b> {start_date}\n"
        "📅 <b>Окончание:</b> {end_date}"
    ),
    "join_contest": "✅ Участвовать",
    "already_joined": "✅ Вы уже участвуете!",
    "joined_success": "🎉 Поздравляем! Вы участвуете в конкурсе!",
    "not_subscribed": (
        "❌ Для участия подпишитесь на следующие каналы:\n\n{channels}\n\n"
        "После подписки нажмите \"🔄 Проверить\"."
    ),
    "check_subscription": "🔄 Проверить",
    "contest_not_active": "❌ Этот конкурс сейчас не активен.",
    "contest_full": "❌ Достигнуто максимальное число участников!",

    "admin_panel": "👑 <b>Админ-панель</b>",
    "create_contest": "➕ Создать конкурс",
    "manage_contests": "📋 Управление конкурсами",
    "statistics": "📊 Статистика",
    "not_admin": "❌ Вы не админ!",

    "enter_title": "📝 Введите название конкурса:",
    "enter_description": "📝 Введите описание конкурса:",
    "enter_prizes": "🎁 Введите призы (например: 1 место: iPhone, 2 место: AirPods):",
    "enter_winners_count": "🏆 Введите количество победителей (например: 3):",
    "enter_max_participants": (
        "👥 Введите максимальное число участников (например: 1000)\n"
        "Или нажмите \"⏭ Пропустить\" для неограниченного:"
    ),
    "enter_start_date": (
        "📅 Введите дату начала.\n"
        "Формат: YYYY-MM-DD HH:MM\n"
        "Например: 2026-05-01 10:00"
    ),
    "enter_end_date": (
        "📅 Введите дату окончания.\n"
        "Формат: YYYY-MM-DD HH:MM\n"
        "Например: 2026-05-10 18:00"
    ),
    "invalid_date": "❌ Неверный формат даты! Попробуйте ещё раз.",
    "invalid_number": "❌ Пожалуйста, введите число!",
    "add_channels": (
        "📢 Теперь добавьте обязательные каналы.\n\n"
        "Бот должен быть <b>админом</b> в канале!\n\n"
        "Отправьте @username или invite-ссылку канала.\n"
        "Для завершения отправьте /done."
    ),
    "channel_added": "✅ Канал добавлен: {title}\n\nДобавьте ещё или нажмите /done.",
    "channel_error": "❌ Не удалось добавить канал. Убедитесь, что бот является админом.",
    "contest_created": (
        "✅ <b>Конкурс создан!</b>\n\n"
        "ID: <code>{id}</code>\n"
        "Название: {title}\n\n"
        "Нажмите \"🚀 Запустить\" для старта."
    ),
    "start_contest": "🚀 Запустить конкурс",
    "contest_started": "🎉 Конкурс запущен! ID: {id}",
    "already_started": "⚠️ Конкурс уже запущен!",

    "select_contest": "📋 Выберите конкурс:",
    "contest_status_draft": "📝 Черновик",
    "contest_status_active": "🟢 Активен",
    "contest_status_finished": "🔴 Завершён",
    "contest_status_cancelled": "⚫️ Отменён",
    "manage_buttons_start": "🚀 Запустить",
    "manage_buttons_finish": "🏁 Завершить",
    "manage_buttons_winners": "🎲 Выбрать победителей",
    "manage_buttons_participants": "👥 Участники",
    "manage_buttons_delete": "🗑 Удалить",
    "confirm_delete": "⚠️ Точно удалить?",
    "deleted": "✅ Удалено!",

    "no_participants": "😔 Нет участников!",
    "winners_selected": "🎉 <b>Победители выбраны!</b>\n\n{winners}",
    "winner_line": "{position}. {name} (@{username}) — ID: <code>{user_id}</code>",
    "winner_no_username": "{position}. {name} — ID: <code>{user_id}</code>",
    "contest_finished_notify": (
        "🏆 <b>Конкурс завершён!</b>\n\n"
        "Конкурс: {title}\n\n"
        "Победители:\n{winners}"
    ),
    "you_are_winner": (
        "🎉 <b>Поздравляем! Вы заняли {position}-е место!</b>\n\n"
        "🏆 Конкурс: {title}\n\n"
        "Для получения приза свяжитесь с админом:\n{admin_contact}"
    ),
    "you_lost": (
        "😔 К сожалению, конкурс <b>{title}</b> завершён.\n\n"
        "На этот раз вам не удалось победить. Участвуйте активнее в следующих конкурсах и займите призовое место! 💪"
    ),

    "stats_text": (
        "📊 <b>Статистика</b>\n\n"
        "👥 Пользователи: {users}\n"
        "🎉 Всего конкурсов: {contests}\n"
        "🟢 Активных: {active}\n"
        "🏆 Завершённых: {finished}"
    ),

    "max_reached_notify": "⚠️ Конкурс {id} достиг максимума участников. Используйте /winner для выбора победителей.",
    "winner_command_usage": "Использование: /winner <contest_id>",
    "help_text": (
        "ℹ️ <b>Помощь</b>\n\n"
        "Этот бот предназначен для Telegram-конкурсов.\n\n"
        "<b>Для пользователей:</b>\n"
        "• Смотрите список активных конкурсов\n"
        "• Подписывайтесь на каналы и участвуйте\n"
        "• Станьте победителем!\n\n"
        "<b>Для админов:</b>\n"
        "/admin - Админ-панель\n"
        "/winner <id> - Выбрать победителей"
    ),
}
