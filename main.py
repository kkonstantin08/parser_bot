import telebot
from telebot.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton
import re

TOKEN = '6857807889:AAF8htzSCtHxQgCFSh7M9lqolRf5hHVj-Do'
bot = telebot.TeleBot(TOKEN)

pattern_wb = r'https:\/\/www\.wildberries\.ru\/catalog\/\d+\/detail\.aspx'
chat_id = ''
mrkt = 0  # индикатор того, что пользователь выбрал маркет плейс или нет. 0 - нет, 1 - да
wanna_price_ind = 0  # индификатор о том, что пользователь ввел желаемую цену. 0 - не ввел, 1 - ввел


"""Надо сделать"""

# ограничесния на добаление товара в день/неделю и т.п.
# описание функционала бота при первом вхождении в бота
# проверка на то, чтобы пользователь вводил сначала желаемую цену, а потом верхнюю
# поставить регулярку на верный url
# написать регулярку для ссылок вб, озон и Яндекс маркета

@bot.message_handler(commands=['start'])  # TODO: сделать обработчик, чтобы пользователь нажимал кнопки только в том порядке, что мне нужно
def send_welcome(message):
    # TODO: можно отправлять картинку с приветствием
    global chat_id
    user_name = message.from_user.first_name
    chat_id = message.chat.id
    user_id = message.from_user.id
    keyboard = InlineKeyboardMarkup(row_width=3)  # поиграться с параметром
    item1 = InlineKeyboardButton('📦Корзина', callback_data='trash')  # TODO: по нажатия нужно доставать все товары из
    # бд для конретного пользователя
    item2 = InlineKeyboardButton('➕Добавить товар', callback_data='add')
    item3 = InlineKeyboardButton('🤖О боте', callback_data='bot')
    keyboard.add(item1, item2, item3)
    bot.send_message(chat_id, f'Главное меню {user_name}', reply_markup=keyboard)
    # TODO: Проверка есть ли пользователь в бд. Если его нет, то занести в бд


@bot.message_handler(content_types=['text'])
def echo_message(message):
    global chat_id, wanna_price_ind
    if 'www.wildberries.ru' in message.text:  # проверка на корректность и присутствие надписи wb в ссылке
        bot.send_message(chat_id, 'right link')
        keyboard = InlineKeyboardMarkup(row_width=3)  # изменить параметр если что-то не будет рабоать
        item1 = InlineKeyboardButton(f'✅Wildberris', callback_data='market_place')  # изменить параметр кол бек дата
        item2 = InlineKeyboardButton('✅Ссылка', callback_data='link')
        item3 = InlineKeyboardButton('Желаемая цена', callback_data='wanna_price')
        item4 = InlineKeyboardButton('Верхняя цена', callback_data='high_price')
        keyboard.add(item1, item2, item3, item4)
        bot.delete_message(message.chat.id, message.message_id - 1)  # удаление прошлых двух сообщений
        bot.delete_message(message.chat.id, message.message_id - 2)
        bot.send_message(chat_id, 'Введите желаемую цену⬇', reply_markup=keyboard)
        # if re.match(pattern_wb, message.text):
        #     print("Ссылка принята!")
        #     keyboard = InlineKeyboardMarkup(row_width=3)  # изменить параметр если что-то не будет рабоать
        #     item1 = InlineKeyboardButton(f'✅Wildberris', callback_data='market_place')  # изменить параметр кол бек дата
        #     item2 = InlineKeyboardButton('✅Ссылка', callback_data='link')
        #     item3 = InlineKeyboardButton('Желаемая цена', callback_data='wanna_price')
        #     item4 = InlineKeyboardButton('Верхняя цена', callback_data='high_price')
        #     keyboard.add(item1, item2, item3, item4)
        #     bot.send_message(chat_id, 'Введите желаемую цену⬇', reply_markup=keyboard)  # сделать обработчик чтобы пользователь ввел сначала
        #     # желаемую цену, а не верхнюю
        # else:
        #     print("Неверная ссылка")
    # TODO: также повторить с озоном и яндекс маркетом
    if message.text.isdigit() and wanna_price_ind == 0:
        keyboard = InlineKeyboardMarkup(row_width=3)  # изменить параметр если что-то не будет рабоать
        item1 = InlineKeyboardButton(f'✅Wildberris', callback_data='market_place')  # изменить параметр кол бек дата
        item2 = InlineKeyboardButton('✅Ссылка', callback_data='link')
        item3 = InlineKeyboardButton(f'✅Желаемая цена={message.text}', callback_data='wanna_price')
        item4 = InlineKeyboardButton('Верхняя цена', callback_data='high_price')
        keyboard.add(item1, item2, item3, item4)
        bot.delete_message(message.chat.id, message.message_id - 1)  # удаление прошлых двух сообщений
        bot.delete_message(message.chat.id, message.message_id - 2)
        bot.send_message(chat_id, 'Введите верхнюю цену⬇', reply_markup=keyboard)
        wanna_price_ind = 1
    if message.text.isdigit() and wanna_price_ind != 0:
        keyboard = InlineKeyboardMarkup(row_width=3)  # изменить параметр если что-то не будет рабоать
        item1 = InlineKeyboardButton('ℹИнформация', callback_data='info')
        item2 = InlineKeyboardButton('Добавить товар', callback_data='add')
        item3 = InlineKeyboardButton('Главное меню', callback_data='menu')
        keyboard.add(item1, item2, item3)
        bot.delete_message(message.chat.id, message.message_id - 1)  # удаление прошлых двух сообщений
        bot.delete_message(message.chat.id, message.message_id - 2)
        bot.send_message(chat_id, 'Готово!', reply_markup=keyboard)
        wanna_price_ind = 0
        # TODO: на этом этапе все данные о товаре даолжы быть занесены уже в бд


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global smiles
    global chat_id
    if call.data == 'add':
        keyboard = InlineKeyboardMarkup(row_width=3)  # изменить параметр если что-то не будет рабоать
        item1 = InlineKeyboardButton(f'Маркетплейс', callback_data='market_place')  # BEAUTY: добавить значок корзины
        item2 = InlineKeyboardButton('Ссылка', callback_data='link')
        item3 = InlineKeyboardButton(f'Желаемая цена', callback_data='wanna_price')
        item4 = InlineKeyboardButton('Верхняя цена', callback_data='high_price')
        keyboard.add(item1, item2, item3, item4)
        bot.send_message(chat_id, 'Выберите маркетплейс', reply_markup=keyboard)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    if call.data == 'market_place':  # добавить индикатор проверки выбора маркетплейса
        kb = InlineKeyboardMarkup(row_width=3)  # поиграться с параметром
        item1 = InlineKeyboardButton('Wildberris', callback_data='wb')
        item2 = InlineKeyboardButton('Ozon', callback_data='ozon')
        item3 = InlineKeyboardButton('Yandex Market', callback_data='ya')
        kb.add(item1, item2, item3)
        bot.send_message(chat_id, 'Добавление товара', reply_markup=kb)
        bot.send_message(chat_id, 'Выберите маркетплейс')
        bot.answer_callback_query(call.id, f'Выберите маркетплейс')
        bot.delete_message(call.message.chat.id, call.message.message_id)
    if call.data == 'wb':
        keyboard = InlineKeyboardMarkup(row_width=3)  # изменить параметр если что-то не будет рабоать
        item1 = InlineKeyboardButton(f'{smiles["yes"]}Wildberris', callback_data='market_place')  # изменить параметр кол бек дата
        item2 = InlineKeyboardButton('Ссылка', callback_data='link')
        item3 = InlineKeyboardButton('Желаемая цена', callback_data='wanna_price')
        item4 = InlineKeyboardButton('Верхняя цена', callback_data='high_price')
        keyboard.add(item1, item2, item3, item4)
        bot.send_message(chat_id, 'Добавление товара', reply_markup=keyboard)
        bot.send_message(chat_id, 'Пришлите ссылку⬇')
        bot.answer_callback_query(call.id, f'Пришлите ссылку')
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.delete_message(call.message.chat.id, call.message.message_id + 1)
    if call.data == 'info':
        # TODO: вывести одним сообщением инфорацию о занесенном товаре и добавить возможность изменения данных
        pass
    if call.data == 'menu':
        keyboard = InlineKeyboardMarkup(row_width=3)  # поиграться с параметром
        item1 = InlineKeyboardButton('📦Корзина', callback_data='trash')
        item2 = InlineKeyboardButton('➕Добавить товар', callback_data='add')
        item3 = InlineKeyboardButton('🤖О боте', callback_data='bot')
        keyboard.add(item1, item2, item3)
        bot.send_message(chat_id, f'Главное меню', reply_markup=keyboard)
        bot.delete_message(call.message.chat.id, call.message.message_id)

bot.infinity_polling()
