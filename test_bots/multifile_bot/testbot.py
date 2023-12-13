import logging
from aiogram import executor
from create_bot import dp                   # импортируем диспетчер из файла-инициализатора бота
from sql_base import sqlite_db              # импортируем из папки с базой файл с указаниями

# логирование
logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    # функция старта бота и запуска БД                                                                
    print('Бот - On-line')
    sqlite_db.sql_start()


from handlers import client, admin, other   # импортируем все хендлеры из заранее созданного файла


'''                              Клиентская часть                                 '''
# вызов функции из соответствующего файла client.py, реализация в многофайловом варианте
client.register_handlers_client(dp)                                                      

'''                              Административная часть                           '''
# вызов функции из соответствующего файла admin.py, реализация в многофайловом варианте                   
admin.register_handlers_admin(dp)       

'''                              Общая часть                                      '''
# вызов функции из соответствующего файла other.py, реализация в многофайловом варианте                   
other.register_handlers_others(dp)                                                       

    
# точка входа
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)        