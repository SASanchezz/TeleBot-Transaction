# Libraries
import Data
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

# from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Constants
start_currency = ''
# Set
logging.basicConfig(level=logging.INFO)
bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())
#Yes/Not
button_yes = KeyboardButton('Yeah')
button_not = KeyboardButton('Nope')
Yes_Not = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_yes, button_not)
#Reload keyboard
button = KeyboardButton('/start')
restart = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button)
# Type of keyboard
button_full = KeyboardButton('All')
button_part = KeyboardButton('Main')
keyboard_type = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_full, button_part)

# Some currency
keyboard_short = ReplyKeyboardMarkup(one_time_keyboard=True)
keyboard_short.add('USA Dollar', 'Euro')
keyboard_short.add('British Pound', 'Japanese Yen')
keyboard_short.add('Polish Zloty', 'Czech Koruna')
keyboard_short.add('Russian Ruble', 'Ukrainian Hryvna')
for num in range(0, len(Data.short['Currency']), 2):
    keyboard_short.add(Data.short['Currency'][num], Data.short['Currency'][num+1])
# All currency
keyboard_long = ReplyKeyboardMarkup(one_time_keyboard=True)
# Keyboard with values
keyboard_long.add('USA Dollar')
for num in range(0, len(Data.long['Currency'])-4, 5):
    keyboard_long.add(Data.long['Currency'][num], Data.long['Currency'][num+1],
Data.long['Currency'][num+2], Data.long['Currency'][num+3], Data.long['Currency'][num+4])
keyboard_long.add('British Pound', 'Ukrainian Hryvna', 'Venezuelan Bolivar')

# Starting keyboard
"""
first_button = KeyboardButton('Из гривны в ...')  # state 1
second_button = KeyboardButton('Из ... в гривну')  # state 2
keyboard0 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(first_button, second_button)
"""
# Few options of exchanging
"""
case1 = lambda message: message.text == 'Из гривны в ...'  # state 1
case2 = lambda message: message.text == 'Из ... в гривну'  # state 2
"""

# Try to make state with class/OOP

class Option(StatesGroup):
    first = State()
    second = State()
    third = State()
    forth = State()
    prefirst = State()


# Start command
@dp.message_handler(commands=['start'], state="*")
async def start(message: Message, state: FSMContext):
    await message.answer('Сколько валют нужно?',
                         reply_markup=keyboard_type)
    await Option.first.set()

# FIRST STAGE
@dp.message_handler(state=Option.first, content_types=ContentTypes.TEXT)
async def from_gryvna(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await state.update_data(keyboard_type=message.text)
    if message.text == 'All':
        main_keyboard = keyboard_long
    elif message.text == 'Main':
        main_keyboard = keyboard_short
    else:
        message.answer('Чё за херь?', reply_markup=restart)
    await message.answer('Input initial currency',
                             reply_markup=main_keyboard)
    await Option.second.set()




# SECOND STAGE
@dp.message_handler(state=Option.second, content_types=ContentTypes.TEXT)
async def amount1(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await state.update_data(first_currency=message.text)
    if user_data['keyboard_type'] == 'All':
        main_keyboard = keyboard_long
    elif user_data['keyboard_type'] == 'Main':
        main_keyboard = keyboard_short
    else:
        message.answer('Чё за херь?', reply_markup=restart)

    await message.answer('Input final currency',
                         reply_markup=main_keyboard)

    await Option.third.set()




#THIRD STAGE
@dp.message_handler(state=Option.third, content_types=ContentTypes.TEXT)
async def currency1(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await state.update_data(final_currency=message.text)
    await message.answer('Input amount(coins after dot (.))')

    await Option.forth.set()



#FORTH STAGE
@dp.message_handler(state=Option.forth, content_types=ContentTypes.TEXT)
async def finish1(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await state.update_data(amount=message.text)

    From_strt_to_dlr = float(list(Data.tables.loc[Data.long.Currrency == user_data['first_currency'], 'To_dollar'])[0].split()[0])

    From_dlr_to_fnsh = float(list(Data.tables.loc[Data.long.Currency == user_data['final_currency'], 'From_dollar'])[0].split()[0])

    Sum = round(user_data['amount'] / Change, 5)
    await message.answer('Ну... Вот:   {0} {1}ов'.format(Sum1, user_data['currency']),
                                                             reply_markup=restart)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)