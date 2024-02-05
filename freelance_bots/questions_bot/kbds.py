from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton

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