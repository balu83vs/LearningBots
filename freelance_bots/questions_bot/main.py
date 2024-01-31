import logging

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.fsm.context import FSMContext

from config import TOKEN

from db_create import db_create
from db_operations import (
                       new_user_creating, check_admin_permissions, get_users_from_database,
                       get_current_question_id, get_next_question, get_question_from_database,
                       save_answer, save_question)

help = """
Справочная информация о программе
будет заполнена позже.
"""

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

db_create()

# стартовая функция бота
async def on_startup(_):                                                               
    await print('Бот - On-line')
    await db_create()

# Обработчик команды /help
@dp.message(Command("help"))
async def start(message: types.Message):
    await message.answer(help)

# Обработчик команды /start
@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    if new_user_creating(user_id):
        await message.answer("Привет! Я бот для рассылки вопросов.\n Ваш user_id успешно внесен в базу данных.\n")
    else:
        await message.answer("Вы уже есть в Базе.")


###################################### начало блока машины состояний #################################################
class FSMAdmin(StatesGroup):
    team_id = State()
    question = State()
    type = State()        

# Обработчик команды /sendall (запуск машины состояний)
@dp.message(StateFilter(None), Command("sendall"))
async def enter_team_id(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    # проверка прав доступа
    if not check_admin_permissions(user_id):
        await message.answer(f"Пользователь {user_id} не является администратором")
    else: 
        await message.answer('Введите айди команды, для которой отправить вопрос.')
        await state.set_state(FSMAdmin.team_id)

# Обработчик команды выхода из машины состояний
@dp.message(Command("exit"))
async def cancel_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if check_admin_permissions(user_id):             
        curent_state = await state.get_state()                            
        if curent_state is None:                                         
            return
        await state.finish()                                                
        await message.reply('OK')     

# функция загрузки team_id в словарь
@dp.message(FSMAdmin.team_id)                                 
async def enter_question(message : types.Message, state: FSMContext):      
    user_id = message.from_user.id
    if check_admin_permissions(user_id):     
        await state.update_data(team_id=message.text)                                  
        await message.answer('Введите вопрос.')
        await state.set_state(FSMAdmin.question)                     

# функция загрузки question в словарь
@dp.message(FSMAdmin.question)                                 
async def enter_type(message : types.Message, state: FSMContext):      
    user_id = message.from_user.id
    if check_admin_permissions(user_id):                                       
        await state.update_data(question=message.text)                                  
        await message.answer('Введите тип вопроса.')
        await state.set_state(FSMAdmin.type)  

# функция загрузки type в словарь
@dp.message(FSMAdmin.type)                                 
async def enter_type(message : types.Message, state: FSMContext):      
    user_id = message.from_user.id
    if check_admin_permissions(user_id):                                       
        await state.update_data(type=message.text)   
        data = await state.get_data()                              
        if save_question(data):
            await state.clear()
            await message.answer('Вопрос успешно сохранен в базе.')
        else:
            await message.answer('Ошибка при сохранении вопроса.')    

###################################### завершение блока машины состояний #################################################


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
    await dp.start_polling(bot, on_startup=on_startup)

if __name__ == "__main__":
    asyncio.run(main())    
