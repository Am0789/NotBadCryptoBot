import telebot
from config import keys, token
from extentions import APIException, CryptoConverter


bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help']) #обработчик показывает инструкции
def help(message: telebot.types.Message):
    text = 'Я твой не самый плохой помощник, и я помогу тебе посчитать твои денежки)\
Напиши валюты в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\n Список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values']) #обработчик показывает валюты
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ]) #обработчик показывает результат конверсии
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Слишком много параметров.')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибочка вышла у пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не пойму что делать, давай заново\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()