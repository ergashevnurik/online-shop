from aiogram import types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from loader import dp, db
from handlers.user.menu import orders
from filters import IsAdmin

@dp.message_handler(IsAdmin(), text=orders)
async def process_orders(message: Message):
    
    orders = db.fetchall('SELECT * FROM orders')
    
    if len(orders) == 0:
        await message.answer('У вас нет заказов.')
    else:
        await order_answer(message, orders)


async def order_answer(message, orders):

    builder = ReplyKeyboardMarkup()


    change_status = InlineKeyboardMarkup()
    change_status.add(types.InlineKeyboardButton(
        text="Поменять статус на уже в пути!",
        callback_data="on_the_way_go")
    )

    res = ''

    for order in orders:
        res += f'Заказ <b>№{order[3]}</b>\nИмя:<b>{order[1]}</b>\nАдрес:<b>{order[2]}</b>\n------------\n'
        builder.add(KeyboardButton(text=f"Имя:{order[1]}"))
    await message.answer(res, reply_markup=builder)

