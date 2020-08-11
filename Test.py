#Libraries
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ContentTypes, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot_token
import logging
#Libraries


logging.basicConfig(level=logging.INFO)
bot = Bot(token = bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())

class Option(StatesGroup):
    kind = State()
    amount1 = State()
    for_start = State()

first_button1 = KeyboardButton('For smth')
second_button1 = KeyboardButton('Another one')
keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(first_button1, second_button1, )

first_button = KeyboardButton('First_button') #state 1
second_button = KeyboardButton('Second_button') #state 2
keyboard0 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(first_button, second_button, )

#Start command
@dp.message_handler(commands= ['start'], state="*")
async def start(message: Message, state: FSMContext):
    await message.answer('Choose button',
                         reply_markup=keyboard0)
    await Option.for_start.set()

@dp.message_handler(state=Option.for_start, content_types=ContentTypes.TEXT)
async def start2(message: Message, state: FSMContext):
    await message.answer('lol',
                         reply_markup=keyboard1)
    await Option.kind.set()

    # FIRST CASE
@dp.message_handler(state=Option.kind)
async def from_gryvna(message: Message):
    await message.answer("DONE")
    print("There")

"""
    #SECOND CASE
@dp.message_handler(state=Option.kind_of_transaction2, content_types=ContentTypes.TEXT)
async def to_gryvna(message: Message, state: FSMContext):
    print("There2")
    if message.text == 'First_button':
        await state.update_data(transaction_option=message.text)
        await message.answer('Any')"""


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


