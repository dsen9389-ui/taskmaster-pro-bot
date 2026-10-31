import aiosqlite
import os
from config import settings

async def init_db():
    os.makedirs(os.path.dirname(settings.DB_PATH), exist_ok=True)
    async with aiosqlite.connect(settings.DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL
            )
        """)
        await db.commit()

async def get_tasks(user_id: int):
    async with aiosqlite.connect(settings.DB_PATH) as db:
        async with db.execute("SELECT id, title FROM tasks WHERE user_id = ?", (user_id,)) as cursor:
            return await cursor.fetchall()

async def add_task(user_id: int, title: str):
    async with aiosqlite.connect(settings.DB_PATH) as db:
        await db.execute("INSERT INTO tasks (user_id, title) VALUES (?, ?)", (user_id, title))
        await db.commit()

async def delete_task(task_id: int):
    async with aiosqlite.connect(settings.DB_PATH) as db:
        await db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        await db.commit()