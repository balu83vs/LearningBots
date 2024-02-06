import logging
import asyncio

from aiogram import Bot, Dispatcher, types

from aiogram.filters.command import Command
from aiogram.filters.state import State, StatesGroup, StateFilter

from aiogram.fsm.context import FSMContext

from config import TOKEN

from db_create import db_create
from db_operations import (
                       new_user_creating, get_users, check_admin_permissions, 
                       save_question, get_question, del_question,
                       save_answer, 
                       save_message, get_message)

from kbds import get_keyboard

help = """
Справочная информация о программе
будет заполнена позже.
"""

user_kb_yesno = get_keyboard(
    'yes',
    'no',
    placeholder='Ответьте Да или Нет',
    sizes=(2,)
)

user_kb_range = get_keyboard(
    '1',
    '2',
    '3',
    '4',
    '5',
    placeholder='Выберите цифру',
    sizes=(5,)
)

admin_kb_yesno = get_keyboard(
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

db_create()

# стартовая функция бота (не работает)
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
        await message.answer('Отправить?', reply_markup=admin_kb_yesno)                                
        await state.set_state(FSMAdmin_question.exit)    

# функция подтверждения отправки вопроса и выхода из FSM
@dp.message(FSMAdmin_question.exit)                                 
async def exit_fsm(message : types.Message, state: FSMContext):      
    user_id = message.from_user.id
    if check_admin_permissions(user_id):    
        if message.text == 'Да':
            data = await state.get_data() 
            try:
                save_question(data)
            except Exception as err:
                await message.answer(f'Ошибка при сохранении вопроса в БД. {err}')
            else:
                team_id = data.get("team_id")
                users = get_users(team_id)
                question = get_question()[0]
                if question[2] == 1:
                    keyboard = user_kb_yesno
                else:
                    keyboard = user_kb_range    
                for user_id in users:
                    await bot.send_message(user_id[0], question[1], reply_markup=keyboard)    
            finally:
                await state.clear()
        elif message.text == 'Нет':
            await message.answer('Вопрос не был отправлен и не сохранен в БД')  
            await state.clear()   
        else:
            await message.answer('Ответ не корректный. Воспользуйтесь клавиатурой')                                  
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
        await message.answer('Отправить?', reply_markup=admin_kb_yesno)                                
        await state.set_state(FSMAdmin_message.exit)    

# функция подтверждения отправки сообщения и выхода из FSM
@dp.message(FSMAdmin_message.exit)                                 
async def exit_fsm(message : types.Message, state: FSMContext):      
    user_id = message.from_user.id
    if check_admin_permissions(user_id):    
        if message.text == 'Да':
            data = await state.get_data() 
            try:
                save_message(data)
            except Exception as err:
                await message.answer(f'Ошибка при сохранении сообщения в БД. {err}')
            else:
                team_id = data.get("team_id")
                users = get_users(team_id)
                message = get_message()[0]   
                for user_id in users:
                    await bot.send_message(user_id[0], message[1])    
            finally:
                await state.clear()
        elif message.text == 'Нет':
            await message.answer('Сообщение не было отправлено и не сохранено в БД')  
            await state.clear()   
        else:
            await message.answer('Ответ не корректный. Воспользуйтесь клавиатурой')                                  
###################### завершение блока машины состояний - отправка сообщения ####################


# Обработчик ответа на вопрос
@dp.message()
async def handle_answer(message: types.Message):
    try:
        question_id = get_question()[0][0]
    except:
        await message.answer('Актуальных вопросов не найдено')    
    else:
        answer = message.text
        if answer in ['yes', 'no', '1', '2', '3', '4', '5']:
            try:            
                save_answer(question_id, answer)
            except Exception as err:
                await message.answer(f'Ошибка при сохранении ответа в БД: {err}')
            else:
                del_question(question_id)    
                await message.answer('Спасибо за ваш ответ!')
        else:
            await message.answer('Ответ не корректный. Воспользуйтесь клавиатурой')   


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot, on_startup=on_startup)

if __name__ == "__main__":
    asyncio.run(main())    
