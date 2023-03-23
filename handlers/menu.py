from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InputMediaPhoto

from keyboards.menu import calculate, main_keyboard, count_keyboard, menu_cd, select_cd


async def start(msg: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data["Розетки"] = 0
        data["Выключатели"] = 0
        data["Бра"] = 0
        data["Потолочный свет"] = 0
        data["Штробление стен"] = 0

    photo = "https://ремонт-павловский-посад.рф/wp-content/uploads/2018/05/777.jpg"
    caption = "Бот для расчета стоимости\n" \
              "электрической сети в квартире."
    await msg.answer_photo(photo=photo, caption=caption, reply_markup=calculate)

async def calculate_net(call: types.CallbackQuery, state: FSMContext, *args, **kwargs):

    markup = await main_keyboard(state)
    caption = "Выберите категорию:"
    media = InputMediaPhoto(caption=caption,
                            media="https://ремонт-павловский-посад.рф/wp-content/uploads/2018/05/777.jpg")
    await call.message.edit_media(media=media, reply_markup=markup)

async def enter_count(call: types.CallbackQuery, state: FSMContext, count_name,  callback_data, *args, **kwargs):

    photo = {
        "Розетки": "https://zakaz64.ru/upload/iblock/c56/c56186551643e58f3abe2b73c715cdbd.jpeg",
        "Выключатели": "https://deshevo-stroi.ru/images/stories/virtuemart/category/viklyuchatel.jpg",
        "Бра": "https://dom-decora.ru/upload/iblock/712/712f61c642f1dd223643fb37080b4430.jpg",
        "Потолочный свет": "https://www.svetlux.ru/images/pics1/products/7/9/9/b/799b6ec588d45e91b8774eb254ca80b7.jpg",
        "Штробление стен": "https://fast.shkola-remonta.com/wp-content/uploads/drilling.jpg"
    }

    async with state.proxy() as data:
        count_name = callback_data["count_name"]
        if callback_data["select"] == "pos":
            data[count_name] += 1
        elif callback_data["select"] == "neg":
            data[count_name] -= 1
    if data[count_name] < 0:
        await call.answer(text="Меньше 0 указать нельзя!", show_alert=True)
        async with state.proxy() as data:
            data[count_name] = 0
    else:
        caption = f"{count_name} - {data[count_name]}"
        media = InputMediaPhoto(caption=caption,
                                media=photo[count_name])
        markup = await count_keyboard(state, count_name)
        await call.message.edit_media(media=media, reply_markup=markup)

async def navigate(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    current_level = callback_data.get('level')
    callback_data: dict
    count_name = callback_data.get('count_name')
    state: FSMContext

    levels = {
                "0": calculate_net,
                "1": enter_count
             }
    current_level_function = levels[current_level]

    await current_level_function(call, state, count_name, callback_data)
    await call.answer()

async def final_count(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        soket = data["Розетки"]
        switch = data["Выключатели"]
        bra = data["Бра"]
        seiling_light = data["Потолочный свет"]
        shtroblenie_walls = data["Штробление стен"]
    text = f"Итоговый расчет:\n" \
           f"розетки\n" \
           f"кабель = 4.35м * {soket} = {4.35*soket}м * 180р. = {int(4.35*soket*180)}р"
    await call.message.answer(text=text)


def register_menu(dp: Dispatcher):
    dp.register_message_handler(start, commands="start")
    dp.register_callback_query_handler(calculate_net, text="calculate")
    dp.register_callback_query_handler(navigate, menu_cd.filter())
    dp.register_callback_query_handler(final_count, text="final")
