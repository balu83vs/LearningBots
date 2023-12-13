from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# кнопки пользовательской клавиатуры
b1 = KeyboardButton('/Режим_работы')
b2 = KeyboardButton('/Расположение')
b3 = KeyboardButton('/Список_детей')
b4 = KeyboardButton('Поделиться номером', request_contact=True)
b5 = KeyboardButton('Где я', request_location=True)

# пользовательская клавиатура (с включенным масштабированием)
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

# пользовательская клавиатура (с включенным масштабированием и автоскрытием с возможностью восстановить) 
# kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) 

# добавление кнопок пользовательской клавиатуры
# kb_client.add(b1).add(b2).add(b3)                                     # кнопки клавиатуры одна под другой
# kb_client.add(b1).add(b2).insert(b3)                                  # кнопки клавиатуры одна под другой и одна справа на той же строчке 
# kb_client.row(b1, b2, b3).row(b4, b5)                                 # 3 кнопки на одной строке и две на другой
kb_client.row(b1, b2, b3)                                              # все кнопки в одну строку
