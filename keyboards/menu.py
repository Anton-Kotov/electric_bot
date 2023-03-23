from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

calculate = InlineKeyboardMarkup()
calculate.insert(InlineKeyboardButton(text="Произвести расчет",
                                      callback_data="calculate"))

menu_cd = CallbackData("calc", "level", "count_name", "select")
select_cd = CallbackData("sel", "count_name", "select")

async def main_keyboard(state: FSMContext):
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=2)
    count_name = ("Розетки", "Выключатели", "Бра", "Потолочный свет", "Штробление стен")

    for i in range(len(count_name)):
        name = count_name[i]

        async with state.proxy() as data:
            count = data[name]

        button_text = f"{name} - {count}"
        callback_data = menu_cd.new(level=CURRENT_LEVEL + 1, count_name=name,
                                    select=0)

        markup.insert(InlineKeyboardButton(text=button_text,
                                      callback_data=callback_data))
    markup.row(InlineKeyboardButton(
        text="РАСЧИТАТЬ", callback_data="final"))
    return markup


async def count_keyboard(state: FSMContext, count_name):

    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=2)
    count_name2 = ("-", "+")
    callback_name = ("neg", "pos")

    for i in range(len(count_name2)):
        name = count_name2[i]

        button_text = name
        callback_data = menu_cd.new(level=CURRENT_LEVEL,
                                    count_name=count_name,
                                    select=callback_name[i])

        markup.insert(InlineKeyboardButton(text=button_text,
                                           callback_data=callback_data))
    markup.insert(InlineKeyboardButton(
            text="Назад", callback_data=menu_cd.new(level=CURRENT_LEVEL - 1,
                                    count_name=count_name,
                                    select=0)))

    return markup

