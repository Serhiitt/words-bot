import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

async def get_db():
    return await asyncpg.connect(DATABASE_URL)

async def init_db():
    conn = await get_db()
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS words (
            id SERIAL PRIMARY KEY,
            word TEXT UNIQUE NOT NULL
        )
    """)
    await conn.close()

async def add_word(word):
    conn = await get_db()
    await conn.execute("INSERT INTO words (word) VALUES ($1) ON CONFLICT DO NOTHING", word)
    await conn.close()

async def get_words():
    conn = await get_db()
    words = await conn.fetch("SELECT word FROM words")
    await conn.close()
    return [row["word"] for row in words]

async def delete_word(word):
    conn = await get_db()
    result = await conn.execute("DELETE FROM words WHERE word = $1", word)
    await conn.close()
    return result

async def clear_words():
    conn = await get_db()
    await conn.execute("DELETE FROM words")
    await conn.close()
