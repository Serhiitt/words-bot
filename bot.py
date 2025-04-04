import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
import database

# Завантаження конфігурації
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Команда для додавання слова
@dp.message(Command("add"))
async def add_word(message: Message):
    word = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
    if not word:
        return await message.reply("⚠ Введи слово після `/add слово`")
    
    await database.add_word(word)
    await message.reply(f"✅ Слово `{word}` додано!")

# Команда для отримання списку слів
@dp.message(Command("list"))
async def list_words(message: Message):
    words = await database.get_words()
    if words:
        await message.reply("📜 Список слів:\n" + "\n".join(words))
    else:
        await message.reply("📭 У базі немає слів!")

# Команда для видалення слова
@dp.message(Command("delete"))
async def delete_word(message: Message):
    word = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
    if not word:
        return await message.reply("⚠ Введи слово після `/delete слово`")

    result = await database.delete_word(word)
    if result == "DELETE 1":
        await message.reply(f"🗑 Слово `{word}` видалено!")
    else:
        await message.reply(f"⚠ Слово `{word}` не знайдено!")

# Команда для очищення бази
@dp.message(Command("clear"))
async def clear_db(message: Message):
    await database.clear_words()
    await message.reply("🧹 База даних очищена!")

# Запуск бота
async def main():
    await database.init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

