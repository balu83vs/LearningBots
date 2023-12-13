from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Text
from config import TOKEN, PHOTOS
import random

from keyboards import KB1, KB2, IKB1                                        # импортируем клавиатуры из отдельного файла

bot = Bot(token = TOKEN)
dp = Dispatcher(bot = bot)

HELP = """
<b>Список_команд</b> - список команд
<b>Главное_меню</b> - главное меню
<b>Меню_фотографий</b> - меню фотографий

"""
photo_key_history = ''
like_flag = False
dislike_flag = False


async def on_start(_):
    # функция предстартовой проверки
    print('Бот запущен успешно')


@dp.message_handler(commands= ['start'])
async def start_bot(message: types.Message):
    # функция обработки команды start
    await bot.send_message(
        chat_id = message.from_user.id, 
        text='Добро пожаловать в наш бот', 
        reply_markup=KB1
        )  
    await message.delete() 


@dp.message_handler(Text(equals = 'Главное_меню'))
async def main_menu(message: types.Message):
    # функция обработки команды Главное_меню
    await bot.send_message(
        chat_id = message.from_user.id, 
        text='Главное меню', 
        reply_markup=KB1
        )  
    await message.delete()      


@dp.message_handler(Text(equals = 'Список_команд'))
async def help(message: types.Message):
    # функция обработки команды Список_команд
    await bot.send_message(
        chat_id = message.from_user.id, 
        text = HELP, 
        parse_mode='HTML'
        )    
    await message.delete()


@dp.message_handler(Text(equals = 'Меню_фотографий'))
async def photos_menu(message: types.Message):
    # функция обработки команды Меню фотографии
    await bot.send_message(
        chat_id = message.from_user.id, 
        text = 'Меню фотографии', 
        reply_markup=KB2
        )      


@dp.message_handler(Text(equals = 'Случайное_фото'))
async def random_photo(message: types.Message):
    # функция обработки команды Случайное_фото
    random_photo_key, photo = random_photo()
    await bot.send_photo(
        chat_id = message.from_user.id, 
        photo= photo, 
        caption = random_photo_key, 
        reply_markup=IKB1
        )          


@dp.callback_query_handler()
async def random_photo_menu(callback: types.CallbackQuery):
    # функция обработки инлайн клавиатуры
    global like_flag
    global dislike_flag
    if callback.data == 'next_photo':
        random_photo_key, photo = random_photo()
        like_flag = False
        dislike_flag = False
        await callback.message.edit_media(types.InputMedia(media=photo, type='photo', caption = random_photo_key), reply_markup=IKB1)
        #await callback.message.answer_photo(photo= photo, caption = random_photo_key, reply_markup=IKB1) # новая картинка в новом сообщении
    if callback.data == 'like':
        if like_flag == False:
            like_flag = True
            dislike_flag = False
            await callback.answer(text='Вам понравилась эта фото')                  # без сообщения, а просто всплывающий текст
            #await callback.message.reply(text='Вам понравилась эта фото')
            #await callback.message.answer(text='Вам понравилась эта фото')   
        else:  
            await callback.answer(text='Вы уже лайкнули это фото')                  # без сообщения, а просто всплывающий текст 
            #await callback.message.answer(text='Вы уже лайкнули это фото')       
    if callback.data == 'dislike':
        if dislike_flag == False:
            like_flag = False
            dislike_flag = True
            await callback.answer(text='Вам не понравилась эта фото')               # без сообщения, а просто всплывающий текст
            #await callback.message.answer(text='Вам не понравилась эта фото') 
        else:   
            await callback.answer(text='Вы уже дизлайкнули это фото')               # без сообщения, а просто всплывающий текст
            #await callback.message.answer(text='Вы уже дизлайкнули это фото')                
        

def random_photo():
    # функция выбора случайной фотографии
    global photo_key_history
    #photo_key = random.choice(list(PHOTOS.keys()))
    curent_list = list(filter(lambda key: key != photo_key_history, list(PHOTOS.keys())))
    photo_key = random.choice(curent_list)
    photo_key_history = photo_key
    photo = PHOTOS.get(photo_key)
    return photo_key, photo

# точка входа
if __name__ == '__main__':
    executor.start_polling(dp, on_startup= on_start, skip_updates=True)
    