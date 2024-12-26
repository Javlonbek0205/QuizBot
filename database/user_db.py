import aiosqlite
import asyncio

class Users:
    def __init__(self, user_id, name:str, chat_id, user_level, points, create_date):
        self.user_id = user_id
        self.name = name
        self.chat_id = chat_id
        self.user_level = user_level
        self.points = points
        self.create_date = create_date

class UserDatabase:
    def __init__(self, db_path='database/UserDb.db'):
        self.db_path = db_path


    async def initialize(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS users(
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(100),
                    chat_id BIGINT UNIQUE,
                    user_level varchar(50),
                    points INT DEFAULT 0,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                ''')
            await db.commit()

    async def add_user(self, name, chat_id, user_level, points):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
            INSERT INTO users(name, chat_id, user_level, points)
            VALUES (?, ?, ?, ?)
            ''', (name, chat_id, user_level, points))
            await db.commit()

    async def change_user(self, chat_id, user_level):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
            UPDATE users SET user_level = ? WHERE chat_id = ?''', (user_level, chat_id))
            await db.commit()

    async def delete_user(self, chat_id):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
            DELETE FROM users where chat_id = ?''', (chat_id,))
            await db.commit()

    async def get_info(self, chat_id):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('''
            SELECT name, user_level, points FROM users where chat_id = ?''', (chat_id,))
            rows = await cursor.fetchone()  # Faqat bitta natijani olish uchun fetchone()
            return rows

    async def update_name(self, name, chat_id):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
            UPDATE users SET name = ? WHERE chat_id = ?''', (name, chat_id))
            await db.commit()

    async def get_user(self):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT chat_id FROM users')
            rows = await cursor.fetchall()
            chat_ids = [row[0] for row in rows]  # Har bir qatordan faqat birinchi elementni (chat_id) olish
            return chat_ids

    async def add_points(self, chat_id, points):
        async with aiosqlite.connect(self.db_path) as db:
            pass


async def create_database():
    db = UserDatabase()
    await db.initialize()


