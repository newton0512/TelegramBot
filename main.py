import telebot
from config import TOKEN, currency
from extensions import CurrenciesConverter, ConvertException


bot = telebot.TeleBot(TOKEN)


# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    msg = 'Я понимаю команды вида: _<имя валюты> <в какую валюту перевести> <сумма>_. \n \
Для просмотра списка доступных валют введите: /values.'
    bot.reply_to(message, msg, parse_mode='Markdown')


# Обрабатывается сообщение с командой '/values'.
@bot.message_handler(commands=['values'])
def handle_start_help(message):
    msg = '*Доступные валюты:*\n\u2705 ' + '\n\u2705 '.join((c[0] + ' (' + c[1] + ')') for c in currency.items())
    bot.send_message(message.chat.id, msg, parse_mode='Markdown')


# Обрабатываются команды конвертации
@bot.message_handler(content_types=['text'])
def handle_convert(message):
    try:
        values = message.text.split(' ')
        if len(values) < 3:
            raise ConvertException('Слишком мало параметров в команде!')

        if len(values) > 3:
            raise ConvertException('Слишком много параметров в команде!')

        msg = CurrenciesConverter.convert(values)
    except ConvertException as e:
        bot.reply_to(message, f'Неверная команда боту.\n_{e}_', parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n_{e}_', parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, msg, parse_mode='Markdown')


bot.polling(none_stop=True)
