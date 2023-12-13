import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage               # самое простое хранилище в оперативной памяти для машины состояний (не БД)

storage = MemoryStorage()                                                  # экземпляр класса хранилища             

bot = Bot(token=os.getenv('TOKEN'))                                        # берем токен не из файла, а из переменной виртуального окружения
dp = Dispatcher(bot, storage=storage)                                      # указание на место хранения