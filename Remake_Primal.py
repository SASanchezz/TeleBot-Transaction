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
button_full = KeyboardButton('All (56)')
button_part = KeyboardButton('4 main')
keyboard_type = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_full, button_part)
# Some currency
keyboard_short = ReplyKeyboardMarkup(one_time_keyboard=True)
keyboard_short.row('доллар', 'евро')
keyboard_short.row('рубль', 'фунт стерлингов')
# All currency
keyboard_long = ReplyKeyboardMarkup(one_time_keyboard=True)  # Keyboard with values
keyboard_long.row('доллар', 'евро', 'рубль', 'фунт стерлингов', 'швейцарский франк', 'польский злотый', 'японская йена')
keyboard_long.row('канадский доллар', 'австралийский доллар', 'грузинский лари', 'молдавский лей', 'китайский юань',
              'датская крона', 'норвежская крона')
keyboard_long.row('шведская крона', 'новый белорусский рубль', 'чешская крона', 'израильский шекель', 'казахстанский тенге',
              'венгерский форинт', 'сингапурский доллар')
keyboard_long.row('азербайджанский манат', 'алжирский динар', 'армянский драм', 'бангладешская така', 'болгарский лев',
              'бразильский реал', 'вьетнамский донг')
keyboard_long.row('ганский седи', 'гонконгский доллар', 'египетский фунт', 'марокканский дирхам', 'индийская рупия',
              'индонезийская рупия', 'иракский динар')
keyboard_long.row('иранский риал', 'кыргызстанский сом', 'южнокорейская вона', 'ливанский фунт', 'ливийский динар',
              'малайзийский ринггит', 'мексиканское песо')
keyboard_long.row('новозеландский доллар', 'дирхам оаэ', 'румынский лей', 'саудовский риал', 'сербский динар',
              'таджикский сомони', 'тайский бат')
keyboard_long.row('новый тайваньский доллар', 'тунисский динар', 'новый манат', 'турецкая лира', 'узбекский сум',
              'филиппинское песо', 'хорватская куна')
# Starting keyboard
first_button = KeyboardButton('Из гривны в ...')  # state 1
second_button = KeyboardButton('Из ... в гривну')  # state 2
keyboard0 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(first_button, second_button)
# Few options of exchanging
case1 = lambda message: message.text == 'Из гривны в ...'  # state 1
case2 = lambda message: message.text == 'Из ... в гривну'  # state 2


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
    await message.answer('Выбери тип перевода',
                         reply_markup=keyboard0)
    await Option.prefirst.set()


#Choose quantity of currency
@dp.message_handler(state=Option.prefirst, content_types=ContentTypes.TEXT)
async def start(message: Message, state: FSMContext):
    await state.update_data(transaction_option=message.text)
    await message.answer('Сколько валют нужно?',
                         reply_markup=keyboard_type)
    await Option.first.set()

# FIRST STAGE
@dp.message_handler(state=Option.first, content_types=ContentTypes.TEXT)
async def from_gryvna(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await state.update_data(keyboard_type=message.text)
    if message.text == 'All (56)':
        main_keyboard = keyboard_long
    elif message.text == '4 main':
        main_keyboard = keyboard_short
    else:
        message.answer('Чё за херь?', reply_markup=restart)
    if user_data['transaction_option'] == 'Из гривны в ...':
        await message.answer('Введите количество грн (копейки через точку)')

    if user_data['transaction_option'] == 'Из ... в гривну':
        await message.answer('Введите начальную валюту',
                             reply_markup=main_keyboard)
    await Option.second.set()




# SECOND STAGE
@dp.message_handler(state=Option.second, content_types=ContentTypes.TEXT)
async def amount1(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if user_data['keyboard_type'] == 'All (56)':
        main_keyboard = keyboard_long
    elif user_data['keyboard_type'] == '4 main':
        main_keyboard = keyboard_short
    else:
        message.answer('Чё за херь?', reply_markup=restart)

    if user_data['transaction_option'] == 'Из гривны в ...':
        try:
            message1 = float(message.text)
            await state.update_data(amount=message1)
            await message.answer('Введите конечную валюту',
                                 reply_markup=main_keyboard)
        except ValueError:
            await message.answer('Ты дурак? Я же просил кол-во')
            await message.answer('Я пока что не шарю как решать такие проблемы, поэтому просто перезапусти через /start',
                                 reply_markup=restart)

    if user_data['transaction_option'] == 'Из ... в гривну':
        if message.text in list(Data.tables['Full_name']):
            await state.update_data(currency=message.text)
            await message.answer('Введите количество грн (копейки через точку)')
        else:
            await message.answer('Ты не ту валюту или вообще число ввёл, идиот. Перезапускай, чё смотришь?',
                                 reply_markup=restart)

    await Option.third.set()




#THIRD STAGE
@dp.message_handler(state=Option.third, content_types=ContentTypes.TEXT)
async def currency1(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if user_data['transaction_option'] == 'Из гривны в ...':
        if message.text in list(Data.tables['Full_name']):
            await state.update_data(currency=message.text)
            await message.answer('Перевести {0} грн в {1} ?'.format(user_data['amount'], message.text),
                                 reply_markup=Yes_Not)
        else:
            await message.answer('Ты не ту валюту или вообще число ввёл, идиот. Перезапускай, чё смотришь?',
                                 reply_markup=restart)

    if user_data['transaction_option'] == 'Из ... в гривну':
        try:
            message2 = float(message.text)
            await state.update_data(amount=message2)
            await message.answer('Перевести {0} {1}а в грн ?'.format(message2, user_data['currency']),
                                 reply_markup=Yes_Not)
        except ValueError:
            await message.answer('Это не число, дегенерат. Перезапускай',
                                 reply_markup=restart)
    await Option.forth.set()



#FORTH STAGE
@dp.message_handler(state=Option.forth, content_types=ContentTypes.TEXT)
async def finish1(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if message.text == "Nope":
        await message.answer('Что тебе уже не так, гнида?',
                             reply_markup=restart)
    if message.text == 'Yeah':   #Calculation
        Change = float(list(Data.tables.loc[Data.tables.Full_name == user_data['currency'].lower(), 'In_grivnas'])[0].split()[0])

        if user_data['transaction_option'] == 'Из гривны в ...':
            Sum1 = round(user_data['amount'] / Change, 5)
            await message.answer('Ну... Вот:   {0} {1}ов'.format(Sum1, user_data['currency']),
                                                                 reply_markup=restart)

        elif user_data['transaction_option'] == 'Из ... в гривну':
            Sum2 = round(user_data['amount'] * Change, 5)
            await message.answer('Ну... Вот:   {} грн'.format(Sum2),
                                 reply_markup=restart)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
