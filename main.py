import os
import re
import telebot
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


bot = telebot.TeleBot(os.environ.get('TOKEN'))


@bot.message_handler(commands=['start'], content_types=['text'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я чат-бот поддержки магазина HexaShop.\n'
                                      'Чтобы наши сотрудники связались с вами, отправьте сообщение в следующем формате:'
                                      '\n<Ваша электронная почта>\n<Текст обращения>\n\n'
                                      'Пожалуйста, не используйте переносы строк в тексте, чтобы мы могли лучше понять '
                                      'ваше сообщение.\nПример:\nexample@example.com\n'
                                      'Хочу рассказать вам, что вы прекрасны :)')


@bot.message_handler(content_types=['text'])
def sendRequest(message):
    text = message.text.split('\n')
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    email = text[0].strip().lower()
    text = '\n'.join(text[1:]).strip()
    if re.match(regex, email):
        data = {
            'email': email,
            'text': text,
        }
        response = requests.post(url=os.environ.get('BACK_URL'), data=data)
        bot.send_message(message.chat.id, 'Ваше сообщение принято\n\nПожалуйста дождитесь ответа на электронную почту. '
                                          'Мы обязательно поможем вам в течении 24-х часов!'
                                          'Спасибо за обращение!')
    else:
        bot.send_message(message.chat.id, 'Введите корректный адрес электронной почты')


bot.polling(non_stop=True, interval=0)
