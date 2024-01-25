import logging
import sqlite3
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from config import TOKEN
from functions import (get_current_question_id, get_next_question, 
                       get_question_from_database, get_users_from_database)


# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot = bot)

# Подключение к базе данных SQLite
conn = sqlite3.connect('answers.db')
cursor = conn.cursor()

# Создание таблицы для сохранения ответов
cursor.execute('''
    CREATE TABLE IF NOT EXISTS answers (
        user_id INTEGER,
        question_id INTEGER,
        answer TEXT,
        PRIMARY KEY (user_id, question_id)
    )
''')
conn.commit()

# Обработчик команды /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Я бот для рассылки вопросов. Введите /send для начала рассылки.")

# Обработчик команды /send
@dp.message(Command("send"))
async def send_questions(message: types.Message):
    # Получаем список пользователей
    users = get_users_from_database()  # Реализуйте эту функцию для получения списка пользователей из базы данных

    # Отправляем вопросы каждому пользователю
    for user_id in users:
        question = get_question_from_database()  # Реализуйте эту функцию для получения вопроса из базы данных
        buttons = [types.KeyboardButton(answer) for answer in question['answers']]
        keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard_markup.add(*buttons)
        await bot.send_message(user_id, question['text'], reply_markup=keyboard_markup)

# Обработчик ответов на вопросы
@dp.message()
async def handle_answer(message: types.Message):
    user_id = message.from_user.id
    question_id = get_current_question_id(user_id)  # Реализуйте эту функцию для получения текущего вопроса пользователя
    answer = message.text

    # Сохраняем ответ в базе данных
    cursor.execute('''
        INSERT OR REPLACE INTO answers (user_id, question_id, answer)
        VALUES (?, ?, ?)
    ''', (user_id, question_id, answer))
    conn.commit()

    # Получаем следующий вопрос
    next_question = get_next_question(question_id)  # Реализуйте эту функцию для получения следующего вопроса
    if next_question:
        buttons = [types.KeyboardButton(answer) for answer in next_question['answers']]
        keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard_markup.add(*buttons)
        await bot.send_message(user_id, next_question['text'], reply_markup=keyboard_markup)
    else:
        await bot.send_message(user_id, "Спасибо за ответы!")


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())    
