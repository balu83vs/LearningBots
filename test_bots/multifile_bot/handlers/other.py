import json, string 

from aiogram import types, Dispatcher
from create_bot import dp


#@dp.message_handler()                                                  # нужен только в однофайловом варианте!!!   
# пустой handler - без команд, перехватывает все команды, которые не нашли свои handler
async def mat_filter(message: types.Message):
    # функция фильтрации матных слов
    text_dict = {el.lower().translate(str.maketrans('', '', string.punctuation)) for el in message.text.split(' ')}
    if text_dict.intersection(set(json.load(open('mat.json')))) != set():
        await message.reply('Без мата!!!')
        await message.delete()


# при многофайловой реализации проекта, нужно зарегистрировать наши хендлеры
def register_handlers_others(dp : Dispatcher):
    dp.register_message_handler(mat_filter)    