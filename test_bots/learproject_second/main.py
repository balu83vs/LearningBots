from aiogram import Bot, Dispatcher, executor, types
from keyboards import IKB
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

async def on_start(_):
    print('Бот запущен успешно!')
   
                

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_start)