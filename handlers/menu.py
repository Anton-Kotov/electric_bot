from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from keyboards.menu import calculate, main_keyboard


async def start(msg: types.Message):
    photo = "https://ремонт-павловский-посад.рф/wp-content/uploads/2018/05/777.jpg"
    caption = "Бот для расчета стоимости\n" \
              "электрической сети в квартире."
    await msg.answer_photo(photo=photo, caption=caption, reply_markup=calculate)

async def calculate_net(call: types.CallbackQuery, state: FSMContext):

    async with state.proxy() as data:
        data["socket"] = 0
        data["switch"] = 0
        data["bra"] = 0
        data["ceiling_light"] = 0
        data["shtroblenie_walls"] = 0
    category = await main_keyboard(state)
    caption = "Выберите категорию:"
    await call.message.edit_caption(caption=caption, reply_markup=category)



def register_menu(dp: Dispatcher):
    dp.register_message_handler(start, commands="start")
    dp.register_callback_query_handler(calculate_net, text="calculate")