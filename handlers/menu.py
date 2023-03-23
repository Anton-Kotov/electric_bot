from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InputMediaPhoto

from keyboards.menu import calculate, main_keyboard, count_keyboard, menu_cd, select_cd, new_calc
from menu_inf import photo


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

    if "photo" in call.message:
        markup = await main_keyboard(state)
        caption = "Выберите категорию:"
        media = InputMediaPhoto(caption=caption,
                                media="https://ремонт-павловский-посад.рф/wp-content/uploads/2018/05/777.jpg")
        await call.message.edit_media(media=media, reply_markup=markup)
    else:
        markup = await main_keyboard(state)
        caption = "Выберите категорию:"
        photo = "https://ремонт-павловский-посад.рф/wp-content/uploads/2018/05/777.jpg"
        await call.message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

async def enter_count(call: types.CallbackQuery, state: FSMContext, count_name,  callback_data, *args, **kwargs):


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
    text = f"<b>Итоговый расчет:</b>\n" \
           f"---------------------------------\n" \
           f"<b>Розетки</b>\n" \
           f"кабель = {4.35*soket}м * 180р. = {int(4.35*soket*180)}р\n" \
           f"подрозетник = {soket} * 480 = {480 * soket}р\n" \
           f"---------------------------------\n" \
           f"<b>Выключатели</b>\n" \
           f"кабель = {3.85*switch}м * 180р. = {int(3.85*switch*180)}р\n" \
           f"подрозетник = 480р * {switch} = {480 * switch}р\n" \
           f"---------------------------------\n" \
           f"<b>Бра</b>\n" \
           f"кабель = {1.4*bra}м * 180р. = {int(1.4*bra*180)}р\n" \
           f"---------------------------------\n" \
           f"<b>Потолочный свет</b>\n" \
           f"кабель = {1.4*seiling_light}м * 180р. = {int(1.4*seiling_light*180)}р\n" \
           f"закладная = 100р * {seiling_light} = {480 * seiling_light}р\n" \
           f"---------------------------------\n" \
           f"<b>Штробление стен</b>\n" \
           f"кабель = {shtroblenie_walls}м * 180р. = {int(shtroblenie_walls*180)}р"
    cable = int(4.35*soket + 3.85*switch + 1.4*seiling_light + 1.4*bra)
    wall_plate = soket + switch
    text_final = f"Кабель = {cable}м * 180 = {cable * 180}р\n" \
                 f"Подрозетник = {wall_plate}шт * 480 = {wall_plate * 480}р\n" \
                 f"Закладная = {seiling_light}шт * 100 = {seiling_light * 100}\n" \
                 f"Штробление стен = {shtroblenie_walls} * 180 = {shtroblenie_walls * 180}р\n" \
                 f"---------------------------------\n" \
                 f"Всего = <b>{cable * 180 + wall_plate * 480 + seiling_light * 100 + shtroblenie_walls * 180}р</b>"

    async with state.proxy() as data:
        data["Розетки"] = 0
        data["Выключатели"] = 0
        data["Бра"] = 0
        data["Потолочный свет"] = 0
        data["Штробление стен"] = 0

    await call.message.answer(text=text)
    await call.message.answer(text=text_final, reply_markup=new_calc)
    await call.answer()



def register_menu(dp: Dispatcher):
    dp.register_message_handler(start, commands="start")
    dp.register_callback_query_handler(calculate_net, text="calculate")
    dp.register_callback_query_handler(navigate, menu_cd.filter())
    dp.register_callback_query_handler(final_count, text="final")
