import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN
from database import db
from handlers import user, admin

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def auto_check_contests(bot: Bot):
    """
    Har daqiqada ishlaydigan vazifa:
    - Sanasiga ko'ra konkurslarni avtomatik boshlash
    - Tugash sanasi kelgan konkurslarni tugatish va g'oliblarni aniqlash
    """
    try:
        now = datetime.now()
        async with db.pool.acquire() as conn:
            # Boshlash vaqti kelgan draft konkurslarni aktivlashtirish
            to_start = await conn.fetch("""
                SELECT id FROM contests 
                WHERE status = 'draft' AND start_date <= $1
            """, now)
            for row in to_start:
                await db.update_contest_status(row['id'], 'active')
                logger.info(f"Contest {row['id']} auto-started")

            # Tugash vaqti kelgan aktiv konkurslarni tugatish
            to_finish = await conn.fetch("""
                SELECT id FROM contests 
                WHERE status = 'active' AND end_date <= $1
            """, now)
            for row in to_finish:
                # Avtomatik g'oliblarni aniqlash
                from handlers.admin import pick_and_announce_winners
                from config import ADMIN_IDS
                admin_id = ADMIN_IDS[0] if ADMIN_IDS else None
                if admin_id:
                    await pick_and_announce_winners(bot, row['id'], admin_id)
                    logger.info(f"Contest {row['id']} auto-finished")
    except Exception as e:
        logger.exception(f"auto_check_contests error: {e}")


async def main():
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("❌ BOT_TOKEN belgilanmagan! .env faylini to'ldiring")
        return

    # Bazaga ulanish
    logger.info("Connecting to database...")
    await db.connect()
    logger.info("✅ Database connected")

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Routerlarni ulash (admin birinchi!)
    dp.include_router(admin.router)
    dp.include_router(user.router)

    # Scheduler (avtomatik vazifalar)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(auto_check_contests, 'interval', minutes=1, args=[bot])
    scheduler.start()
    logger.info("✅ Scheduler started")

    try:
        logger.info("🚀 Bot started!")
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        scheduler.shutdown()
        await bot.session.close()
        await db.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
