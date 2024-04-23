import os
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command


from sql_base_runner import data_input, data_output


API_TOKEN = os.getenv("TELEGRAM_TOKEN")


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot)


@dp.message(Command("start"))
async def welcome(message: types.Message):
    """Отправляет приветственное сообщение"""

    await message.answer(f'Здравствуй, {message.from_user.full_name}!')


@dp.message()
async def query_input(message: types.Message):
    """
    Универсальный запрос
    """
    control_query = message.text.split('  ')
    if len(control_query) == 2:
        control = message.text.split('  ')[0]
        query = message.text.split('  ')[1]
        if control == '/to_db':
            try:
                data_input(query)
            except Exception as err:
                await message.answer("Ошибка при внесении")
                await message.answer(err)
            else:
                await message.answer("Данные успешно внесены в БД")
        elif control == '/from_db':
            try:
                data = data_output(query)
            except Exception as err:
                await message.answer("Ошибка в запросе")
                await message.answer(f'{err}')
            else:
                await message.answer("Запрос успешно обработан")
                await message.answer(f'Данные: {data}')
        else:
            await message.answer("Неизвестная управляющая команда")
    else:
        await message.answer("Неправильный формат запроса")

    



# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())