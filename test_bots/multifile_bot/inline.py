import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text  # встроенный фильтр текста
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# берем токен не из файла, а из переменной виртуального окружения
bot = Bot(
    token=os.getenv("TOKEN")
)  

dp = Dispatcher(bot)

# словарь для голосования
golos_dict = dict()  

async def on_startup(_):
    # функция старта бота и запуска БД
    print("Бот - On-line")


# кнопки ссылки и клавиатура, состоящая из них в разных конфигурациях расположения
urlkb = InlineKeyboardMarkup(row_width=2)  # задаем толщину клавиатуры
urlButton = InlineKeyboardButton(text="Кнопка 1", url="https://youtube.com")  # определяем первую кнопку
urlButton2 = InlineKeyboardButton(text="Кнопка 2", url="https://google.com")  # определяем вторую кнопку

# задаем список из кнопок
list_button = [
    InlineKeyboardButton(text="Кнопка 3", url="https://youtube.com"),
    InlineKeyboardButton(text="Кнопка 4", url="https://google.com"),
]  

# urlkb.add(urlButton, urlButton2).row(*list_button).insert(InlineKeyboardButton(text = 'Кнопка 5', url = 'https://google.com')) # добавляем кнопки разными методами

inkb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="Нажми меня", callback_data="www"))  # кнопка с выбросом метки www при нажатии


@dp.message_handler(commands="инлайн")
# декоратор для handlerа вызывающего клавиатуру по команде Список ссылок  
async def url_command(message: types.Message):  
    # управляющая функция
    await message.answer("Инлайн кнопка", reply_markup=inkb)  # действие после ввода команды


@dp.callback_query_handler(text="www")  
# хендлер, который ловит факт нажатия инлайн кнопки по выбросу www и выводит некое ообщение
async def www_call(callback: types.CallbackQuery):
    # await callback.message.answer('Нажата инлайн кнопка') # выводит в чат сообщение по нажатию на кнопку
    await callback.answer("Нажата инлайн кнопка", show_alert=True)  # выводит большое окно с сообщением и кнопкой подтверждения
    await callback.answer()                                         # отправляем пустое подтверждение


# простое голосование
golos = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text="Like", callback_data="like_1"),
    InlineKeyboardButton(text="Не Like", callback_data="like_-1"),
)


@dp.message_handler(commands="голосование")  
# декоратор для handlerа вызывающего клавиатуру по команде голосование
async def golos_command(message: types.Message):  
    # управляющая функция
    await message.answer("Простое голосование", reply_markup=golos)  # действие после ввода команды


@dp.callback_query_handler(Text(startswith="like_"))  
# хендлер, который ловит факт нажатия инлайн кнопки и через встроенный фильтр принимает значение 1 или -1 отсекая текст like_
async def www_golos(callback: types.CallbackQuery):
    # управляющая функция
    res = int(callback.data.split("_")[1])
    if f"{callback.from_user.id}" not in golos_dict:
        golos_dict[f"{callback.from_user.id}"] = res
        await callback.answer("Вы проголосовали")
    else:
        await callback.answer("Вы уже проголосовали", show_alert=True)

# точка входа
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
