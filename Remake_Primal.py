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
#from aiogram.contrib.fsm_storage.memory import MemoryStorage

#Constants
start_currency = ''
# Set
logging.basicConfig(level=logging.INFO)
bot = Bot(token = bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())
# All currency
keyboard1 = ReplyKeyboardMarkup() # Keyboard with values
keyboard1.row('доллар', 'евро', 'рубль', 'фунт стерлингов', 'швейцарский франк', 'польский злотый', 'японская йена' )
keyboard1.row('канадский доллар', 'австралийский доллар', 'грузинский лари', 'молдавский лей', 'китайский юань', 'датская крона', 'норвежская крона')
keyboard1.row('шведская крона', 'новый белорусский рубль', 'чешская крона', 'израильский шекель', 'казахстанский тенге', 'венгерский форинт', 'сингапурский доллар')
keyboard1.row('азербайджанский манат', 'алжирский динар', 'армянский драм', 'бангладешская така', 'болгарский лев', 'бразильский реал', 'вьетнамский донг')
keyboard1.row('ганский седи', 'гонконгский доллар', 'египетский фунт', 'марокканский дирхам', 'индийская рупия', 'индонезийская рупия', 'иракский динар')
keyboard1.row('иранский риал', 'кыргызстанский сом', 'южнокорейская вона', 'ливанский фунт', 'ливийский динар', 'малайзийский ринггит', 'мексиканское песо')
keyboard1.row('новозеландский доллар', 'дирхам оаэ', 'румынский лей', 'саудовский риал', 'сербский динар', 'таджикский сомони', 'тайский бат')
keyboard1.row('новый тайваньский доллар', 'тунисский динар', 'новый манат', 'турецкая лира', 'узбекский сум', 'филиппинское песо', 'хорватская куна')
# Starting keyboard
first_button = KeyboardButton('Из гривны в ...') #state 1
second_button = KeyboardButton('Из ... в гривну') #state 2
keyboard0 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(first_button, second_button, )
# Few options of exchanging
case1 = lambda message: message.text == 'Из гривны в ...' #state 1
case2 = lambda message: message.text == 'Из ... в гривну' #state 2
#Try to make state with class/OOP

class Option(StatesGroup):
    kind_of1 = State()
    currency1 = State()
    amount1 = State()

    kind_of2 = State()
    currency2 = State()
    amount2 = State()

    for_start = State()
    finish = State()
#Start command
@dp.message_handler(commands= ['start'], state="*")
async def start(message: Message, state: FSMContext):
    await message.answer('Выбери тип перевода',
                         reply_markup=keyboard0)
    await Option.for_start.set()

@dp.message_handler(state=Option.for_start, content_types=ContentTypes.TEXT)
async def start2(message: Message, state: FSMContext):
    if message.text == 'Из гривны в ...':
        await Option.kind_of1.set()

    if message.text == 'Из ... в гривну':
        await Option.kind_of2.set()
    await state.update_data(transaction_option=message.text)
#From grn to...
@dp.message_handler(state=Option.kind_of1, content_types=ContentTypes.TEXT)
async def from_gryvna(message: Message, state: FSMContext):
    print("There")

    await message.answer('Введите количество грн (копейки через точку)')
    await Option.amount1.set()
#Getting amount
@dp.message_handler(state=Option.amount1, content_types=ContentTypes.TEXT)
async def amount1(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if user_data['transaction_option'] == 'Из гривны в ...':
        await state.update_data(amount=message.text)
        await message.answer('Введите валюту',
                             reply_markup=keyboard1)
        await Option.currency1.set()

@dp.message_handler(state=Option.currency1, content_types=ContentTypes.TEXT)
async def currency1(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if user_data['transaction_option'] == 'Из гривны в ...':
        await Option.finish.set()
        await state.update_data(currency=message.text)
        await message.answer(user_data['transaction_option'])

@dp.message_handler(state=Option.finish, content_types=ContentTypes.TEXT)
async def finish1(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if user_data['transaction_option'] == 'Из гривны в ...':
        await message.answer(user_data['currency'])


#From some currency to grivna
@dp.message_handler(state=Option.kind_of2, content_types=ContentTypes.TEXT)
async def to_gryvna(message: Message, state: FSMContext):
    if message.text == 'Из ... в гривну':
        await state.update_data(transaction_option=message.text)
        await message.answer('Введите валюту',
                            reply_markup=keyboard1)
        await Option.currency2.set()


@dp.message_handler(state=Option.currency2, content_types=ContentTypes.TEXT)
async def currency2(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if user_data['transaction_option'] == 'Из ... в гривну':
        await state.update_data(currency=message.text)
        await message.answer('Введите Введите количество (копейки через точку')
        await Option.amount2.set()


@dp.message_handler(state=Option.amount2, content_types=ContentTypes.TEXT)
async def amount2(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if user_data['transaction_option'] == 'Из ... в гривну':
        await Option.finish.set()
        await state.update_data(amount=message.text)
        await message.answer(user_data['transaction_option'])


@dp.message_handler(state=Option.finish, content_types=ContentTypes.TEXT)
async def finish2(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if user_data['transaction_option'] == 'Из ... в гривну':
        await message.answer(user_data['currency'])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)