import os
import logging

from aiogram import Bot, Dispatcher, executor, types

import exceptions
import expenses
from categories import Categories
from middlewares import AccessMiddleware


logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
ACCESS_ID = int(os.getenv('TELEGRAM_ACCESS_ID'))

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(ACCESS_ID))


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer(
        "Financial accounting bot\n\n"
        "Add expense (example): 12 taxi\n"
        "Today's statistics: /today\n"
        "Statistics for current month: /month\n"
        "Last expenses: /expenses\n"
        "Expense categories: /categories")


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    row_id = int(message.text[4:])
    expenses.delete_expense(row_id)
    answer_message = 'The transaction was deleted'
    await message.answer(answer_message)


@dp.message_handler(commands=['categories'])
async def get_category_list(message: types.Message):
    categories = Categories().get_all_categories()
    print(list(c.aliases for c in categories))
    answer_message = 'Expense categories:\n\n* ' + \
        ('\n* '.join(c.name+' ('+', '.join(c.aliases)+')' for c in categories))
    await message.answer(answer_message)


@dp.message_handler(commands=['today'])
async def get_today_statistics(message: types.Message):
    answer_message = expenses.get_today_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['month'])
async def get_month_statistics(message: types.Message):
    answer_message = expenses.get_month_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['expenses'])
async def get_last_expenses(message: types.Message):
    last_expenses = expenses.get_last_transactions()
    if not last_expenses:
        await message.answer('Nothing to display yet')
        return

    last_expenses_rows = [
        f'{expense.amount} $ for {expense.category_name} — click '
        f'/del{expense.id} to delete'
        for expense in last_expenses
    ]
    answer_message = 'Last transactions:\n\n* ' + '\n\n* '.join(last_expenses_rows)
    await message.answer(answer_message)


@dp.message_handler()
async def add_expense(message: types.Message):
    try:
        expense = expenses.add_expense(message.text)
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return
    answer_message = (
        f'Expense added: {expense.amount} $ for {expense.category_name}.\n\n'
        f'{expenses.get_today_statistics()}')
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
