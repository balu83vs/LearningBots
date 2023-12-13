"""
Машина состояний без использования SQL
"""
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram import Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
import time

ID = None

class FSMAdmin(StatesGroup):                                       
    photo = State()
    name = State()
    description = State()
    age = State()


# Проверка прав администратора (реализована на базе стандартных прав администратора группы Telegram)
#@dp.message_handler(commands = ['moderator'], is_chat_admin = True)    # нужен только в однофайловом варианте!!!   
async def admin_rights(message: types.Message):
    # для проверки администратор должен написать в группу
    global ID 
    ID = message.from_user.id                                           # вытаскиваем id пользователя и проверяем на административность группы
    await bot.send_message(message.from_user.id, 'Административные права подтверждены.') #, reply_markup = button_case_admin)
    await message.delete()


# Базовый handler для запуска машины состояний

#@dp.message_handler(commands = 'Загрузить', state=None)                # нужен только в однофайловом варианте!!!
# бот еще в обычном состоянии, начало входа по команде "Загрузить"
async def cm_start(message : types.Message):
    if message.from_user.id == ID:                                      # проверка соответствия прав администратора
        await FSMAdmin.photo.set()                                      # бот переходит в режим машины состояний и ждет загрузки фото
        await message.reply('Загрузи фото')                             # выдача сообщения пользователю
    else:
        for _ in range(3):
            await bot.send_message(message.from_user.id, 'Нарушение прав доступа!!!')    
            time.sleep(3)


# Ловим первый ответ (загрузку фото) и пишем в словать ID изображения
#@dp.message_handler(content_types = ['photo'], state=FSMAdmin.photo)   # нужен только в однофайловом варианте!!!  
# FSMAdmin.photo это указатель для бота на конкретный handler, в котором расположена функция загрузки фото
async def load_photo(message : types.Message, state: FSMContext):     
    # функция загрузки ID фото в словарь (ее параметры с анотацией)
    if message.from_user.id == ID:                                      # проверка соответствия прав администратора
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()                                           # бот запрашивает следующую позицию машины состояния и ждет ввод name
        await message.reply('Теперь введи название')                    # выдача сообщения пользователю


# Ловим второй ответ (name) и пишем в словать название
#@dp.message_handler(state = FSMAdmin.name)                             # нужен только в монофайловом варианте!!!  
# FSMAdmin.name это указатель для бота на конкретный handler, в котором расположена функция загрузки названия
async def load_name(message : types.Message, state: FSMContext):        
    # функция загрузки name в словарь (ее параметры с анотацией)
    if message.from_user.id == ID:                                      # проверка соответствия прав администратора
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()                                           # бот запрашивает следующую позицию машины состояния и ждет ввод description
        await message.reply('Теперь введи описание')                    # выдача сообщения пользователю


# Ловим третий ответ (description) и пишем в словать описание
#@dp.message_handler(state = FSMAdmin.description)                      # нужен только в монофайловом варианте!!!  
# FSMAdmin.description это указатель для бота на конкретный handler, в котором расположена функция загрузки описания
async def load_description(message : types.Message, state: FSMContext): 
    # функция загрузки description в словарь (ее параметры с анотацией)
    if message.from_user.id == ID:                                      # проверка соответствия прав администратора
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()                                           # бот запрашивает следующую позицию машины состояния и ждет ввод description
        await message.reply('Теперь введи возраст')                     # выдача сообщения пользователю


# Ловим последний ответ (price) и пишем в словать цену
#@dp.message_handler(state = FSMAdmin.age)                              # нужен только в монофайловом варианте!!!  
# FSMAdmin.age это указатель для бота на конкретный handler, в котором расположена функция загрузки цены
async def load_age(message : types.Message, state: FSMContext):      
    # функция загрузки price в словарь (ее параметры с анотацией)
    if message.from_user.id == ID:                                      # проверка соответствия прав администратора
        async with state.proxy() as data:
            data['age'] = float(message.text)
        
        
        async with state.proxy() as data:                               # открываем полученный словарь состояний и данных
            await message.reply(str(data))                              # выдаем всю инфу в чат (как временное решение пока не будет создана загрузка в бвзу данных) 
            
    
    
        await state.finish()                                            # бот выходит из машины состояний и очищает все данные (все операции над данными нужно выполнить до этой команды)


# Выход из машины состояний (нужен обязательно, если пользователь передумал)

# dp.message_handler(state = '*', commands = 'Отмена')                  # нужен только в монофайловом варианте!!! 
# в каком бы state не находился состоянии  (для команды 'Отмена') 
# dp.message_handler(Text(equals = 'Отмена', ignore_case = True), state = '*') # нужен только в монофайловом варианте!!!  
# в каком бы state не находился состоянии  (для текста 'Отмена')
async def cancel_handler(message: types.Message, state: FSMContext):
    # функция выхода из машины состояний
    if message.from_user.id == ID:                                      # проверка соответствия прав администратора
        curent_state = await state.get_state()                          # присвоение переменной текущего состояния машины
        if curent_state is None:                                        # проверка если бот не в состоянии машины,  то ничего завершаем Handler 
            return
        await state.finish()                                            # если в состоянии, все закрываем и выходим из машины состояний
        await message.reply('OK')                                       # выдаем сообщение в чат
 

# при многофайловой реализации проекта, нужно зарегистрировать наши хендлеры машины состояний в функции, для дальнейшего импорта в нужные функции

def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(cm_start, commands = ['Загрузить'], state = None)
    dp.register_message_handler(load_photo, content_types = ['photo'], state = FSMAdmin.photo)
    dp.register_message_handler(load_name, state = FSMAdmin.name)
    dp.register_message_handler(load_description, state = FSMAdmin.description)
    dp.register_message_handler(load_age, state = FSMAdmin.age)
    dp.register_message_handler(cancel_handler, state = '*', commands = 'отмена')                        
    dp.register_message_handler(cancel_handler, Text(equals = 'отмена', ignore_case = True), state = '*')
    dp.register_message_handler(admin_rights, commands = ['moderator'], is_chat_admin = True)
    