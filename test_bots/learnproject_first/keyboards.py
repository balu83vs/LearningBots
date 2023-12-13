from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


KB1 = ReplyKeyboardMarkup(resize_keyboard=True)
b11 = KeyboardButton('Список_команд')
b12 = KeyboardButton('Меню_фотографий')
KB1.add(b11).add(b12)


KB2 = ReplyKeyboardMarkup(resize_keyboard=True)
b21 = KeyboardButton('Главное_меню')
b22 = KeyboardButton('Случайное_фото')
KB2.add(b21).add(b22)

IKB1 = InlineKeyboardMarkup(row_width=3)
ib1 = InlineKeyboardButton(text='следующее фото', callback_data='next_photo')
ib2 = InlineKeyboardButton(text = 'лайк', callback_data='like')
ib3 = InlineKeyboardButton(text = 'дизлайк', callback_data='dislike')
IKB1.add(ib1).add(ib2).insert(ib3)


