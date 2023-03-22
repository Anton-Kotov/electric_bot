from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

calculate = InlineKeyboardMarkup()
calculate.insert(InlineKeyboardButton(text="Произвести расчет",
                                      callback_data="calculate"))

menu_cd = CallbackData("calc", "level", "count_name")

async def main_keyboard(state: FSMContext):
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=2)
    count_name = ("Розетки", "Выключатели", "Бра", "Потолочный свет", "Штробление стен")
    callback_name = ("socket", "switch", "bra", "ceiling_light", "shtroblenie_walls")

    for i in range(len(count_name)):
        name = count_name[i]
        callback = callback_name[i]

        async with state.proxy() as data:
            count = data[callback]

        button_text = f"{name} - {count}"
        callback_data = menu_cd.new(level=CURRENT_LEVEL + 1, count_name=callback)

        markup.insert(InlineKeyboardButton(text=button_text,
                                      callback_data=callback_data))
    return markup

