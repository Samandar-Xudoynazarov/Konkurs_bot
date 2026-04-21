TEXTS = {
    "start": "👋 Hello, {name}!\n\nWelcome to the contest bot!",
    "choose_language": "🌐 Choose your language:",
    "language_changed": "✅ Language changed to English!",
    "main_menu": "🏠 Main menu",
    "back": "◀️ Back",
    "cancel": "❌ Cancel",
    "cancelled": "❌ Cancelled",
    "skip": "⏭ Skip",
    "done": "✅ Done",
    "yes": "✅ Yes",
    "no": "❌ No",

    "active_contests": "🎉 Active contests",
    "my_contests": "📋 My contests",
    "change_language": "🌐 Change language",
    "help": "ℹ️ Help",

    "no_active_contests": "😔 No active contests yet.",
    "contest_info": (
        "🎉 <b>{title}</b>\n\n"
        "📝 {description}\n\n"
        "🎁 <b>Prizes:</b>\n{prizes}\n\n"
        "🏆 <b>Winners count:</b> {winners_count}\n"
        "👥 <b>Participants:</b> {participants}{max_part}\n"
        "📅 <b>Start:</b> {start_date}\n"
        "📅 <b>End:</b> {end_date}"
    ),
    "join_contest": "✅ Participate",
    "already_joined": "✅ You are already participating!",
    "joined_success": "🎉 Congratulations! You are participating!",
    "not_subscribed": (
        "❌ To participate, please subscribe to these channels:\n\n{channels}\n\n"
        "After subscribing, click \"🔄 Check\"."
    ),
    "check_subscription": "🔄 Check",
    "contest_not_active": "❌ This contest is not active.",
    "contest_full": "❌ Maximum participants reached!",

    "admin_panel": "👑 <b>Admin panel</b>",
    "create_contest": "➕ Create contest",
    "manage_contests": "📋 Manage contests",
    "statistics": "📊 Statistics",
    "not_admin": "❌ You are not an admin!",

    "enter_title": "📝 Enter contest title:",
    "enter_description": "📝 Enter contest description:",
    "enter_prizes": "🎁 Enter prizes (e.g., 1st: iPhone, 2nd: AirPods):",
    "enter_winners_count": "🏆 Enter number of winners (e.g., 3):",
    "enter_max_participants": (
        "👥 Enter maximum participants (e.g., 1000)\n"
        "Or click \"⏭ Skip\" for unlimited:"
    ),
    "enter_start_date": (
        "📅 Enter start date.\n"
        "Format: YYYY-MM-DD HH:MM\n"
        "Example: 2026-05-01 10:00"
    ),
    "enter_end_date": (
        "📅 Enter end date.\n"
        "Format: YYYY-MM-DD HH:MM\n"
        "Example: 2026-05-10 18:00"
    ),
    "invalid_date": "❌ Invalid date format! Try again.",
    "invalid_number": "❌ Please enter a number!",
    "add_channels": (
        "📢 Now add required channels.\n\n"
        "Bot must be <b>admin</b> in the channel!\n\n"
        "Send channel @username or invite link.\n"
        "Send /done to finish."
    ),
    "channel_added": "✅ Channel added: {title}\n\nAdd more or press /done.",
    "channel_error": "❌ Failed to add channel. Make sure bot is admin there.",
    "contest_created": (
        "✅ <b>Contest created!</b>\n\n"
        "ID: <code>{id}</code>\n"
        "Title: {title}\n\n"
        "Click \"🚀 Start\" to launch."
    ),
    "start_contest": "🚀 Start contest",
    "contest_started": "🎉 Contest started! ID: {id}",
    "already_started": "⚠️ Contest already started!",

    "select_contest": "📋 Select contest:",
    "contest_status_draft": "📝 Draft",
    "contest_status_active": "🟢 Active",
    "contest_status_finished": "🔴 Finished",
    "contest_status_cancelled": "⚫️ Cancelled",
    "manage_buttons_start": "🚀 Start",
    "manage_buttons_finish": "🏁 Finish",
    "manage_buttons_winners": "🎲 Pick winners",
    "manage_buttons_participants": "👥 Participants",
    "manage_buttons_delete": "🗑 Delete",
    "confirm_delete": "⚠️ Really delete?",
    "deleted": "✅ Deleted!",

    "no_participants": "😔 No participants!",
    "winners_selected": "🎉 <b>Winners selected!</b>\n\n{winners}",
    "winner_line": "{position}. {name} (@{username}) — ID: <code>{user_id}</code>",
    "winner_no_username": "{position}. {name} — ID: <code>{user_id}</code>",
    "contest_finished_notify": (
        "🏆 <b>Contest finished!</b>\n\n"
        "Contest: {title}\n\n"
        "Winners:\n{winners}"
    ),
    "you_are_winner": (
        "🎉 <b>Congratulations! You took {position}th place!</b>\n\n"
        "🏆 Contest: {title}\n\n"
        "To claim your prize, contact the admin:\n{admin_contact}"
    ),
    "you_lost": (
        "😔 Unfortunately, the contest <b>{title}</b> has ended.\n\n"
        "You didn't win this time. Participate more actively in the next contests and claim a prize! 💪"
    ),

    "stats_text": (
        "📊 <b>Statistics</b>\n\n"
        "👥 Users: {users}\n"
        "🎉 Total contests: {contests}\n"
        "🟢 Active: {active}\n"
        "🏆 Finished: {finished}"
    ),

    "max_reached_notify": "⚠️ Contest {id} reached max participants. Use /winner to pick winners.",
    "winner_command_usage": "Usage: /winner <contest_id>",
    "help_text": (
        "ℹ️ <b>Help</b>\n\n"
        "This bot is for Telegram contests.\n\n"
        "<b>For users:</b>\n"
        "• Browse active contests\n"
        "• Subscribe to channels and participate\n"
        "• Become a winner!\n\n"
        "<b>For admins:</b>\n"
        "/admin - Admin panel\n"
        "/winner <id> - Pick winners"
    ),
}
