import asyncpg
from typing import Optional, List
from config import DATABASE_URL


class Database:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        """Bazaga ulanish"""
        self.pool = await asyncpg.create_pool(DATABASE_URL)
        await self.create_tables()

    async def close(self):
        """Bazadan uzilish"""
        if self.pool:
            await self.pool.close()

    async def create_tables(self):
        """Jadvallarni yaratish"""
        async with self.pool.acquire() as conn:
            # Foydalanuvchilar
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    username VARCHAR(255),
                    full_name VARCHAR(255),
                    language VARCHAR(5) DEFAULT 'uz',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Konkurslar
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS contests (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(500) NOT NULL,
                    description TEXT,
                    prizes TEXT,
                    winners_count INTEGER DEFAULT 1,
                    max_participants INTEGER,
                    start_date TIMESTAMP,
                    end_date TIMESTAMP,
                    status VARCHAR(20) DEFAULT 'draft',
                    created_by BIGINT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    finished_at TIMESTAMP
                )
            """)
            # status: draft, active, finished, cancelled

            # Majburiy kanallar
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS contest_channels (
                    id SERIAL PRIMARY KEY,
                    contest_id INTEGER REFERENCES contests(id) ON DELETE CASCADE,
                    channel_id BIGINT NOT NULL,
                    channel_username VARCHAR(255),
                    channel_title VARCHAR(255),
                    channel_link VARCHAR(500)
                )
            """)

            # Ishtirokchilar
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS participants (
                    id SERIAL PRIMARY KEY,
                    contest_id INTEGER REFERENCES contests(id) ON DELETE CASCADE,
                    user_id BIGINT NOT NULL,
                    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(contest_id, user_id)
                )
            """)

            # G'oliblar
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS winners (
                    id SERIAL PRIMARY KEY,
                    contest_id INTEGER REFERENCES contests(id) ON DELETE CASCADE,
                    user_id BIGINT NOT NULL,
                    position INTEGER,
                    selected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    # ========== Foydalanuvchilar ==========
    async def add_user(self, user_id: int, username: str, full_name: str, language: str = 'uz'):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO users (user_id, username, full_name, language)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (user_id) DO UPDATE 
                SET username = $2, full_name = $3
            """, user_id, username, full_name, language)

    async def get_user(self, user_id: int):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow("SELECT * FROM users WHERE user_id = $1", user_id)

    async def set_user_language(self, user_id: int, language: str):
        async with self.pool.acquire() as conn:
            await conn.execute("UPDATE users SET language = $1 WHERE user_id = $2", language, user_id)

    async def get_user_language(self, user_id: int) -> str:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT language FROM users WHERE user_id = $1", user_id)
            return row['language'] if row else 'uz'

    # ========== Konkurslar ==========
    async def create_contest(self, title: str, description: str, prizes: str,
                             winners_count: int, max_participants: Optional[int],
                             start_date, end_date, created_by: int) -> int:
        async with self.pool.acquire() as conn:
            return await conn.fetchval("""
                INSERT INTO contests (title, description, prizes, winners_count, 
                    max_participants, start_date, end_date, created_by, status)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, 'draft')
                RETURNING id
            """, title, description, prizes, winners_count, max_participants,
                start_date, end_date, created_by)

    async def get_contest(self, contest_id: int):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow("SELECT * FROM contests WHERE id = $1", contest_id)

    async def get_active_contests(self):
        async with self.pool.acquire() as conn:
            return await conn.fetch("SELECT * FROM contests WHERE status = 'active' ORDER BY id DESC")

    async def get_all_contests(self):
        async with self.pool.acquire() as conn:
            return await conn.fetch("SELECT * FROM contests ORDER BY id DESC LIMIT 50")

    async def update_contest_status(self, contest_id: int, status: str):
        async with self.pool.acquire() as conn:
            if status == 'finished':
                await conn.execute("""
                    UPDATE contests SET status = $1, finished_at = CURRENT_TIMESTAMP 
                    WHERE id = $2
                """, status, contest_id)
            else:
                await conn.execute("UPDATE contests SET status = $1 WHERE id = $2", status, contest_id)

    async def delete_contest(self, contest_id: int):
        async with self.pool.acquire() as conn:
            await conn.execute("DELETE FROM contests WHERE id = $1", contest_id)

    # ========== Kanallar ==========
    async def add_channel(self, contest_id: int, channel_id: int, username: str,
                          title: str, link: str):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO contest_channels (contest_id, channel_id, channel_username, 
                    channel_title, channel_link)
                VALUES ($1, $2, $3, $4, $5)
            """, contest_id, channel_id, username, title, link)

    async def get_contest_channels(self, contest_id: int):
        async with self.pool.acquire() as conn:
            return await conn.fetch("""
                SELECT * FROM contest_channels WHERE contest_id = $1
            """, contest_id)

    async def remove_channel(self, channel_row_id: int):
        async with self.pool.acquire() as conn:
            await conn.execute("DELETE FROM contest_channels WHERE id = $1", channel_row_id)

    # ========== Ishtirokchilar ==========
    async def add_participant(self, contest_id: int, user_id: int) -> bool:
        async with self.pool.acquire() as conn:
            try:
                await conn.execute("""
                    INSERT INTO participants (contest_id, user_id)
                    VALUES ($1, $2)
                """, contest_id, user_id)
                return True
            except asyncpg.UniqueViolationError:
                return False

    async def is_participant(self, contest_id: int, user_id: int) -> bool:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT 1 FROM participants WHERE contest_id = $1 AND user_id = $2
            """, contest_id, user_id)
            return row is not None

    async def get_participants_count(self, contest_id: int) -> int:
        async with self.pool.acquire() as conn:
            return await conn.fetchval("""
                SELECT COUNT(*) FROM participants WHERE contest_id = $1
            """, contest_id)

    async def get_participants(self, contest_id: int) -> List[int]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT user_id FROM participants WHERE contest_id = $1
            """, contest_id)
            return [row['user_id'] for row in rows]

    # ========== G'oliblar ==========
    async def add_winner(self, contest_id: int, user_id: int, position: int):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO winners (contest_id, user_id, position)
                VALUES ($1, $2, $3)
            """, contest_id, user_id, position)

    async def get_winners(self, contest_id: int):
        async with self.pool.acquire() as conn:
            return await conn.fetch("""
                SELECT w.*, u.username, u.full_name 
                FROM winners w
                LEFT JOIN users u ON w.user_id = u.user_id
                WHERE w.contest_id = $1
                ORDER BY w.position
            """, contest_id)

    async def clear_winners(self, contest_id: int):
        async with self.pool.acquire() as conn:
            await conn.execute("DELETE FROM winners WHERE contest_id = $1", contest_id)


db = Database()
