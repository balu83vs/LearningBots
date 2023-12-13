import time

from aiogram import types
from aiogram import Dispatcher                                                  # для многофайлового варианта нужен этот импорт
from aiogram.types import ReplyKeyboardRemove                                   # импорт библиотеки автоскрытия клавиатуры
from create_bot import dp, bot
from keyboards import kb_client                                                 # импорт переменной клавиатуры

from sql_base import sqlite_db                                                  # импорт файла с описанием БД


#@dp.message_handler(commands=['start', 'help'])                                # прием команд start и help      
async def command_start(message: types.Message):
    try:
        await bot.send_message(
            message.from_user.id, 
            'Приветсвенное сообщение', 
            reply_markup = kb_client
            )                                                                   # вывод сообщения в личку
        await message.delete()
    except:
        await message.reply('Общение с ботом через личку!')


#@dp.message_handler(commands=['Режим_работы'])                                 # прием команд любых других команд, например "Режим работы"      
async def graf_open(message: types.Message):
    await bot.send_message(message.from_user.id, 'С 10 до 18')                  # вывод сообщения в личку
# await message.answer('С 10 до 18')                                            # вывод сообщения в группу


#@dp.message_handler(commands=['Расположение'])                                 # прием команд любых других команд, например "Расположение"      
async def position(message: types.Message):
    await bot.send_message(
        message.from_user.id, 
        'Санкт - Петербург', 
        reply_markup=ReplyKeyboardRemove()
        )                                                                       # вывод сообщения в личку и удаление всей клавиатуры после нажатия 
# await message.answer('Санкт - Петербург')                                     # вывод сообщения в группу


#@dp.message_handler(commands=['Список_детей'])                                 # реакция на нажатие кнопки Список детей      
async def child_list(message: types.Message):
    await sqlite_db.sql_read(message)


# при многофайловой реализации проекта, нужно зарегистрировать наши хендлеры
def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(graf_open, commands=['Режим_работы'])
    dp.register_message_handler(position, commands=['Расположение'])
    dp.register_message_handler(child_list, commands=['Список_детей'])
