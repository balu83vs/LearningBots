import logging

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from config import TOKEN

from db_create import db_create
from db_operations import (
                       new_user_creating, get_users_from_database,
                       get_current_question_id, get_next_question, get_question_from_database,
                       save_answer)


# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot = bot)

# Создание объекта БД
db_create()

# Обработчик команды /start
@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    if new_user_creating(user_id):
        await message.answer("Привет! Я бот для рассылки вопросов.\n Ваш user_id успешно внесен в базу данных.\n")
    else:
        await message.answer("Вы уже есть в Базе.")

# Обработчик команды /send
@dp.message(Command("send"))
async def send_questions(message: types.Message):
    # Получаем список пользователей
    users = get_users_from_database()  # список пользователей из базы данных
    # Отправляем вопросы каждому пользователю
    for user_id in users:
        #question = get_question_from_database()  # вопрос из базы данных
        #buttons = [types.KeyboardButton(answer) for answer in question['answers']]
        #keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        #keyboard_markup.add(*buttons)
        #await bot.send_message(user_id, question['text'], reply_markup=keyboard_markup)
        await bot.send_message(user_id[0], f'Проверка {user_id[0]}')

# Обработчик ответов на вопросы
@dp.message()
async def handle_answer(message: types.Message):
    user_id = message.from_user.id
    question_id = get_current_question_id(user_id)  # текущий вопрос пользователя
    answer = message.text

    # Сохраняем ответ в базе данных
    save_answer(user_id, question_id, answer)

    # Получаем следующий вопрос
    next_question = get_next_question(question_id)  # следующий вопрос
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
