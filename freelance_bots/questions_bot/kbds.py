from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton, InlineKeyboardButton

# конструктор простой клавиатуры
def get_keyboard(
        *btns: str,
        placeholder: str = None,
        sizes: tuple[int] = (2,),
):
    """
    Example:
    get_keyboard(
            "Меню",
            "О магазине",
            placeholder = "Что вас интересует",
            sizes = (2,2,1)
    )
    """
    keyboard = ReplyKeyboardBuilder()
    
    for index, text in enumerate(btns,start=0):
        keyboard.add(KeyboardButton(text = text))

    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard = True, input_field_placeholder = placeholder)


# конструктор inline клавиатуры
def get_inline_keyboard(
        *btns: str,
        placeholder: str = None,
        sizes: tuple[int] = (2,),
):
    inline_keyboard = InlineKeyboardBuilder()
    
    for index, text in enumerate(btns,start=0):
        inline_keyboard.add(InlineKeyboardButton(text = text, callback_data=text))

    return inline_keyboard.adjust(*sizes).as_markup(
        resize_keyboard = True, input_field_placeholder = placeholder)