import Data as dt
import telebot as tl
import pandas as pd
import config as cg
data = dt.tables["Full_name"]
Values = ''

bot = tl.TeleBot(cg.bot_token)

keyboard1 = tl.types.ReplyKeyboardMarkup() # Keyboard with values
keyboard1.row('доллар', 'евро', 'рубль', 'фунт стерлингов', 'швейцарский франк', 'польский злотый', 'японская йена' )
keyboard1.row('канадский доллар', 'австралийский доллар', 'грузинский лари', 'молдавский лей', 'китайский юань', 'датская крона', 'норвежская крона')
keyboard1.row('шведская крона', 'новый белорусский рубль', 'чешская крона', 'израильский шекель', 'казахстанский тенге', 'венгерский форинт', 'сингапурский доллар')
keyboard1.row('азербайджанский манат', 'алжирский динар', 'армянский драм', 'бангладешская така', 'болгарский лев', 'бразильский реал', 'вьетнамский донг')
keyboard1.row('ганский седи', 'гонконгский доллар', 'египетский фунт', 'марокканский дирхам', 'индийская рупия', 'индонезийская рупия', 'иракский динар')
keyboard1.row('иранский риал', 'кыргызстанский сом', 'южнокорейская вона', 'ливанский фунт', 'ливийский динар', 'малайзийский ринггит', 'мексиканское песо')
keyboard1.row('новозеландский доллар', 'дирхам оаэ', 'румынский лей', 'саудовский риал', 'сербский динар', 'таджикский сомони', 'тайский бат')
keyboard1.row('новый тайваньский доллар', 'тунисский динар', 'новый манат', 'турецкая лира', 'узбекский сум', 'филиппинское песо', 'хорватская куна')

keyboard0 = tl.types.ReplyKeyboardMarkup(resize_keyboard = True) # Starting keyboard
keyboard0.row('Из гривны в ...', 'Из ... в гривну')

keyboard3 = tl.types.ReplyKeyboardMarkup()
keyboard3.row('Введите кол-во')

"""greetings = ['дорова', 'привет', 'hi', 'hello', 'здорова']
parting = ['bye', 'goodbye', 'seeya', 'пока', 'прощай', 'я пойду']"""
love = ['i love you', 'i love u', 'love u', 'love you', 'люблю', 'люблю тебя', 'ты лучший' ]



@bot.message_handler(commands=['start'])     #Start command

def start_message (message):
        bot.send_message(message.chat.id, 'Введите тип перевода',
                         reply_markup=keyboard0)


@bot.message_handler(content_types=['text'])   # If text
def send_text(message):
    if message.text == 'Из гривны в ...':
        bot.send_message(message.chat.id, 'Введите в какую валюту',
                         reply_markup = keyboard1)
        if message.text in data:
            bot.send_message(message.chat.id, 'Впишите кол-во (копейки через точку)')

            if (type(message.text) == int or message.text) == float:
                bot.send_message(message.chat.id, 'oil')

        else:
            bot.send_message(message.chat.id, 'Таких валют нет, сори')






    if message.text.lower() == 'Из ... в гривну':
        #for i in data:
        bot.send_message(message.chat.id, data)

    if message.text.lower() in love:
        bot.send_sticker(message.chat.id, 'CAACAgQAAxkBAANfXwWrL71ZrGabdOGN-pxsZD4FMOUAAl4AA10rqQGLmgO0L7-luxoE')

@bot.message_handler(content_types=['sticker'])
def sticker_info(message):
    bot.send_message(message.chat.id, message)
    print(message)

bot.polling()
print(type(data))