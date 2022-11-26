from aiogram import types
from aiogram.types import Message
from loader import dp, db
from .menu import delivery_status
from filters import IsUser

answer = [
    'лежит на складе.',
    'уже в пути!',
    'прибыл и ждет вас на почте!'
]

@dp.message_handler(IsUser(), text=delivery_status)
async def process_delivery_status(message: Message):
    
    orders = db.fetchall('SELECT * FROM orders WHERE cid=?', (message.chat.id,))
    
    if len(orders) == 0:
        await message.answer('У вас нет активных заказов.')
    else:
        await delivery_status_answer(message, orders, answer[0])

async def delivery_status_answer(message, orders, answer):

    res = ''

    for order in orders:

        res += f'Заказ <b>№{order[3]}</b> \n'
        res += 'Статус: ' + answer
        res += '\n'
        res += f'Имя: {order[1]}\n'
        res += f'Адрес: {order[2]}'
        res += '\n-----------\n'

    await message.answer(res)

@dp.message_handler(IsUser(), text='on_the_way_go')
async def change_status(message: Message, callback: types.CallbackQuery):
    orders = db.fetchall('SELECT * FROM orders WHERE cid=?', (message.chat.id,))

    await delivery_status_answer(message, orders, answer[1])

    await callback.answer(text="Спасибо, что воспользовались ботом!", show_alert=True)

