import logging
import asyncio

from aiogram import Bot, Dispatcher, types

from aiogram.filters.command import Command
from aiogram.filters.state import State, StatesGroup, StateFilter

from aiogram.fsm.context import FSMContext

from config import TOKEN

from db_create import db_create
from db_operations import (
                       new_user_creating, 
                       get_team_users, 
                       check_admin_permissions, 
                       save_question, get_question, del_question,
                       save_answer, 
                       save_message, get_message)

from kbds import get_inline_keyboard, get_keyboard

help = """
Бот для рассылки сообщений и вопросов членам определенной команды.\n 
Ответы на вопросы предлагаются членам команды в виде inline кнопок и сохраняются в базе данных.\n
Рассылка вопросов и сообщений инициализируется администратором после ввода определенных команд.\n
Для регистрации нового пользователя введите /start\n
Для получения справки введите /help\n
"""

# стартовая клавиатура
start_keyboard = get_keyboard(
    '/start',
    '/help',
    placeholder='Базовые команды',
    sizes=(1,1)
)


# инлайн клавиатуры пользователя
user_inline_kb_yesno = get_inline_keyboard(
    'yes',
    'no',
    placeholder='Ответьте Да или Нет',
    sizes=(2,)
)

user_inline_kb_range = get_inline_keyboard(
    '1',
    '2',
    '3',
    '4',
    '5',
    placeholder='Выберите цифру',
    sizes=(5,)
)


# инлайн клавиатуры администратора
admin_inline_kb_yesno = get_inline_keyboard(
    'Да',
    'Нет',
    placeholder='Отправить вопрос',
    sizes=(2,)
)


# Настройка логирования
logging.basicConfig(level=logging.INFO)


# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()


# стартовая функция бота (не работает)
async def on_startup(_):                                                               
    await db_create()
    print('Бот - On-line')

db_create() # костыль для запуска БД


# Обработчик команды /help
@dp.message(Command("help"))
async def start(message: types.Message):
    await message.answer(help)


# Обработчик команды /start
@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    await message.answer("Привет! Я бот для рассылки вопросов.", reply_markup=start_keyboard)
    if new_user_creating(user_id):
        await message.answer("Ваш user_id успешно внесен в базу данных.")
    else:
        await message.answer("Вы уже есть в Базе.")


############################# блок машины состояний - отправка вопроса ####################
class FSMAdmin_question(StatesGroup):
    team_id = State()
    question = State()
    type = State()    
    exit = State()    

# Обработчик команды /sendall (запуск машины состояний)
@dp.message(StateFilter(None), Command("sendall"))
async def start_fsm(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    # проверка прав доступа
    if not check_admin_permissions(user_id):
        await message.answer(f"Пользователь {user_id} не является администратором")
    else: 
        await message.answer('Введите айди команды, для которой отправить вопрос.')
        await state.set_state(FSMAdmin_question.team_id)

# Обработчик команды выхода из машины состояний
@dp.message(Command("exit"))
async def cancel_fsm(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if check_admin_permissions(user_id):             
        curent_state = await state.get_state()                            
        if curent_state is None:                                         
            return
        await state.clear()                                               
        await message.answer('Внесение вопроса в базу данных прервано.')    

# функция загрузки team_id в словарь
@dp.message(FSMAdmin_question.team_id)                                 
async def enter_team_id(message : types.Message, state: FSMContext):      
    user_id = message.from_user.id
    if check_admin_permissions(user_id):     
        await state.update_data(team_id=message.text)                                  
        await message.answer('Введите вопрос.')
        await state.set_state(FSMAdmin_question.question)                     

# функция загрузки question в словарь
@dp.message(FSMAdmin_question.question)                                 
async def enter_question(message : types.Message, state: FSMContext):      
    user_id = message.from_user.id
    if check_admin_permissions(user_id):                                       
        await state.update_data(question=message.text)                                  
        await message.answer('Введите тип вопроса.')
        await state.set_state(FSMAdmin_question.type)  

# функция загрузки type в словарь
@dp.message(FSMAdmin_question.type)                                 
async def enter_type(message : types.Message, state: FSMContext):      
    user_id = message.from_user.id
    if check_admin_permissions(user_id):                                       
        await state.update_data(type=message.text)
        await message.answer('Отправить?', reply_markup=admin_inline_kb_yesno)                       
        await state.set_state(FSMAdmin_question.exit)

# функция подтверждения отправки вопроса и выхода из FSM
@dp.callback_query(FSMAdmin_question.exit)                                 
async def exit_fsm(callback: types.CallbackQuery, state: FSMContext):      
    user_id = callback.from_user.id
    if check_admin_permissions(user_id):    
        # введен вариант ответа "Да" 
        if callback.data == 'Да':
            data = await state.get_data() 
            try:
                save_question(data)
            except Exception as err:
                await callback.answer(f'Ошибка при сохранении вопроса в БД. {err}', show_alert=True)
            else:
                team_id = data.get("team_id")
                users = get_team_users(team_id)
                question = get_question()[0]
                if question[2] == 1:
                    keyboard = user_inline_kb_yesno
                else:
                    keyboard = user_inline_kb_range    
                for user_id in users:
                    await bot.send_message(user_id[0], question[1], reply_markup=keyboard) 
                    await callback.answer(f'Вопрос для группы {team_id} успешно отправлено.', show_alert=True)   
            finally:
                await state.clear()
        # введен вариант ответа "Нет"         
        elif callback.data == 'Нет':
            await callback.answer('Вопрос не был отправлен и не сохранен в БД', show_alert=True)  
            await state.clear()   
        else:
            await callback.answer('Ответ не корректный. Воспользуйтесь клавиатурой', show_alert=True)                                  
###################### завершение блока машины состояний - отправка вопроса ##################


###################### блок машины состояний - отправка сообщения ############################
class FSMAdmin_message(StatesGroup):
    team_id = State()
    text_message = State() 
    exit = State()    

# Обработчик команды /sendallmessage (запуск машины состояний)
@dp.message(StateFilter(None), Command("sendallmessage"))
async def start_fsm(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    # проверка прав доступа
    if not check_admin_permissions(user_id):
        await message.answer(f"Пользователь {user_id} не является администратором")
    else: 
        await message.answer('Введите айди команды, для которой отправить сообщение.')
        await state.set_state(FSMAdmin_message.team_id)

# Обработчик команды выхода из машины состояний
@dp.message(Command("exit"))
async def cancel_fsm(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if check_admin_permissions(user_id):             
        curent_state = await state.get_state()                            
        if curent_state is None:                                         
            return
        await state.clear()                                               
        await message.answer('Отправка сообщения команде отменена.')    

# функция загрузки team_id в словарь
@dp.message(FSMAdmin_message.team_id)                                 
async def enter_team_id(message : types.Message, state: FSMContext):      
    user_id = message.from_user.id
    if check_admin_permissions(user_id):     
        await state.update_data(team_id=message.text)                                  
        await message.answer('Введите сообщение.')
        await state.set_state(FSMAdmin_message.text_message)                      

# функция загрузки message в словарь
@dp.message(FSMAdmin_message.text_message)                                 
async def enter_type(message : types.Message, state: FSMContext):      
    user_id = message.from_user.id
    if check_admin_permissions(user_id):                                       
        await state.update_data(text_message=message.text)  
        await message.answer('Отправить?', reply_markup=admin_inline_kb_yesno)                                
        await state.set_state(FSMAdmin_message.exit)    

# функция подтверждения отправки сообщения и выхода из FSM
@dp.callback_query(FSMAdmin_message.exit)                                 
async def exit_fsm(callback : types.CallbackQuery, state: FSMContext):      
    user_id = callback.from_user.id
    if check_admin_permissions(user_id):    
        if callback.data == 'Да':
            data = await state.get_data() 
            try:
                save_message(data, user_id)
            except Exception as err:
                await callback.answer(f'Ошибка при сохранении сообщения в БД. {err}')
            else:
                team_id = data.get("team_id")
                users = get_team_users(team_id)
                message = get_message()[0]   
                for user_id in users:
                    await bot.send_message(user_id[0], message[1])  
                    await callback.answer(f'Сообщение для группы {team_id} успешно отправлено.', show_alert=True)  
            finally:
                await state.clear()
        elif callback.data == 'Нет':
            await callback.answer('Сообщение не было отправлено и не сохранено в БД', show_alert=True)  
            await state.clear()   
        else:
            await callback.answer('Ответ не корректный. Воспользуйтесь клавиатурой', show_alert=True)                                  
###################### завершение блока машины состояний - отправка сообщения ####################


# Обработчик ответа на вопрос
@dp.callback_query()
async def handle_answer(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    try:
        question_id = get_question()[0][0]
    except:
        await callback.answer('Актуальных вопросов не найдено', show_alert=True)    
    else:
        answer = callback.data
        # защита от ручного ввода ответов
        if answer in ['yes', 'no', '1', '2', '3', '4', '5']:
            try:            
                save_answer(question_id, answer, user_id) 
            except Exception as err:
                await callback.answer(f'Ошибка при сохранении ответа в БД: {err}', show_alert=True)
            else:
                del_question(question_id)
                await callback.answer('Спасибо за ваш ответ!', show_alert=True)
        else:
            await callback.answer('Ответ не корректный. Воспользуйтесь клавиатурой', show_alert=True)               


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot, on_startup=on_startup)

if __name__ == "__main__":
    asyncio.run(main())    
