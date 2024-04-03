import re
import telebot
from telebot.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from config import TOKEN


bot = telebot.TeleBot(TOKEN)
engine = create_engine('sqlite:///parser_mrk_plc.db')

Base = declarative_base()


class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    market_place = Column(String, nullable=True, default='test')
    link = Column(String, nullable=True, default='test')
    wanna_price = Column(Integer, nullable=True, default=0)
    high_price = Column(Integer, nullable=True, default=0)


Base.metadata.create_all(bind=engine)

pattern_wb = r'https:\/\/www\.wildberries\.ru\/catalog\/\d+\/detail\.aspx'

"""Надо сделать"""


# ограничесния на добаление товара в день/неделю и т.п.
# описание функционала бота при первом вхождении в бота
# проверка на то, чтобы пользователь вводил сначала желаемую цену, а потом верхнюю
# поставить регулярку на верный url
# написать регулярку для ссылок вб, озон и Яндекс маркета

@bot.message_handler(commands=['start'])  # TODO: сделать обработчик, чтобы пользователь нажимал кнопки только в том порядке, что мне нужно
def send_welcome(message):
    # TODO: можно отправлять картинку с приветствием
    session = Session(bind=engine)
    user_name = message.from_user.first_name
    chat_id = message.chat.id
    user_id = message.from_user.id

    user = session.query(Data).filter_by(user_id=user_id).first()
    if not user:
        session.add(Data(user_id=user_id))
        session.commit()

    keyboard = InlineKeyboardMarkup(row_width=3)  # поиграться с параметром
    item1 = InlineKeyboardButton('📦Корзина', callback_data='trash')  # TODO: по нажатия нужно доставать все товары из
    # бд для конретного пользователя
    item2 = InlineKeyboardButton('➕Добавить товар', callback_data='add')
    item3 = InlineKeyboardButton('🤖О боте', callback_data='bot')
    keyboard.add(item1, item2, item3)
    bot.send_message(chat_id, f'Главное меню {user_name}', reply_markup=keyboard)
    # TODO: Проверка есть ли пользователь в бд. Если его нет, то занести в бд


wanna_price_ind = 0
message_history = ''



@bot.message_handler(content_types=['text'])
def echo_message(message):
    global message_history
    chat_id = message.chat.id
    session = Session(bind=engine)  # открытие сессии
    user = session.query(Data).filter_by(user_id=message.from_user.id).first()

    if not user:
        user = Data(User_id=message.from_user)
        session.add(user)

    elif 'www.wildberries.ru' in message.text:  # проверка на корректность и присутствие надписи wb в ссылке
        user.link = message.text
        session.commit()

        bot.send_message(chat_id, 'right link')
        keyboard = InlineKeyboardMarkup(row_width=3)  # изменить параметр если что-то не будет рабоать
        item1 = InlineKeyboardButton(f'✅Wildberris', callback_data='market_place')  # изменить параметр кол бек дата
        item2 = InlineKeyboardButton('✅Ссылка', callback_data='link')
        item3 = InlineKeyboardButton('Желаемая цена', callback_data='wanna_price')
        item4 = InlineKeyboardButton('Верхняя цена', callback_data='high_price')
        keyboard.add(item1, item2, item3, item4)
        # bot.delete_message(message.chat.id, message.message_id - 1)  # удаление прошлых двух сообщений
        # bot.delete_message(message.chat.id, message.message_id - 2)
        bot.send_message(chat_id, 'Введите желаемую цену⬇', reply_markup=keyboard)
        # if re.match(pattern_wb, message.text): print("Ссылка принята!") keyboard = InlineKeyboardMarkup(row_width=3)  # изменить
        # параметр если что-то не будет рабоать item1 = InlineKeyboardButton(f'✅Wildberris', callback_data='market_place')  # изменить
        # параметр кол бек дата item2 = InlineKeyboardButton('✅Ссылка', callback_data='link') item3 = InlineKeyboardButton('Желаемая
        # цена', callback_data='wanna_price') item4 = InlineKeyboardButton('Верхняя цена', callback_data='high_price') keyboard.add(
        # item1, item2, item3, item4) bot.send_message(chat_id, 'Введите желаемую цену⬇', reply_markup=keyboard)  # сделать обработчик
        # чтобы пользователь ввел сначала # желаемую цену, а не верхнюю else: print("Неверная ссылка")
        message_history = 'Введите желаемую цену⬇'
        print(message_history)

    # TODO: также повторить с озоном и яндекс маркетом
    elif message.text.isdigit() and message_history == 'Введите желаемую цену⬇':
        user.wanna_price = int(message.text)
        session.commit()

        keyboard = InlineKeyboardMarkup(row_width=3)  # изменить параметр если что-то не будет рабоать
        item1 = InlineKeyboardButton(f'✅Wildberris', callback_data='market_place')  # изменить параметр кол бек дата
        item2 = InlineKeyboardButton('✅Ссылка', callback_data='link')
        item3 = InlineKeyboardButton(f'✅Желаемая цена={message.text}', callback_data='wanna_price')
        item4 = InlineKeyboardButton('Верхняя цена', callback_data='high_price')
        keyboard.add(item1, item2, item3, item4)
        # bot.delete_message(message.chat.id, message.message_id - 1)  # удаление прошлых двух сообщений
        # bot.delete_message(message.chat.id, message.message_id - 2)
        bot.send_message(chat_id, 'Введите верхнюю цену⬇', reply_markup=keyboard)
        message_history = 'Введите верхнюю цену⬇'
        print(message_history)

    elif message.text.isdigit() and message_history == 'Введите верхнюю цену⬇':
        user.high_price = int(message.text)
        session.commit()
        print(f'зашел в блок для установки верхней цены. цена {message.text}')
        keyboard = InlineKeyboardMarkup(row_width=3)  # изменить параметр если что-то не будет рабоать
        item1 = InlineKeyboardButton('ℹИнформация', callback_data='info')
        item2 = InlineKeyboardButton('Добавить товар', callback_data='add')
        item3 = InlineKeyboardButton('Главное меню', callback_data='menu')
        keyboard.add(item1, item2, item3)
        # bot.delete_message(message.chat.id, message.message_id - 1)  # удаление прошлых двух сообщений
        # bot.delete_message(message.chat.id, message.message_id - 2)
        message_history = 'Готово'
        print(message_history)
    if message.text.isdigit() and message_history == 'Готово':
        keyboard = InlineKeyboardMarkup(row_width=3)  # изменить параметр если что-то не будет рабоать
        item1 = InlineKeyboardButton('ℹИнформация', callback_data='info')
        item2 = InlineKeyboardButton('Добавить товар', callback_data='add')
        item3 = InlineKeyboardButton('Главное меню', callback_data='menu')
        keyboard.add(item1, item2, item3)
        bot.send_message(chat_id, 'Готово!', reply_markup=keyboard)


        # TODO: на этом этапе все данные о товаре даолжы быть занесены уже в бд


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    chat_id = call.message.chat.id
    if call.data == 'add':
        keyboard = InlineKeyboardMarkup(row_width=3)  # изменить параметр если что-то не будет рабоать
        item1 = InlineKeyboardButton(f'Маркетплейс', callback_data='market_place')  # BEAUTY: добавить значок корзины
        item2 = InlineKeyboardButton('Ссылка', callback_data='link')
        item3 = InlineKeyboardButton(f'Желаемая цена', callback_data='wanna_price')
        item4 = InlineKeyboardButton('Верхняя цена', callback_data='high_price')
        keyboard.add(item1, item2, item3, item4)
        bot.send_message(chat_id, 'Выберите маркетплейс', reply_markup=keyboard)
        # bot.delete_message(call.message.chat.id, call.message.message_id)
    if call.data == 'market_place':  # добавить индикатор проверки выбора маркетплейса
        kb = InlineKeyboardMarkup(row_width=3)  # поиграться с параметром
        item1 = InlineKeyboardButton('Wildberris', callback_data='wb')
        item2 = InlineKeyboardButton('Ozon', callback_data='ozon')
        item3 = InlineKeyboardButton('Yandex Market', callback_data='ya')
        kb.add(item1, item2, item3)
        bot.send_message(chat_id, 'Добавление товара', reply_markup=kb)
        bot.send_message(chat_id, 'Выберите маркетплейс')
        bot.answer_callback_query(call.id, f'Выберите маркетплейс')
        # bot.delete_message(call.message.chat.id, call.message.message_id)
    if call.data == 'wb':
        keyboard = InlineKeyboardMarkup(row_width=3)  # изменить параметр если что-то не будет рабоать
        item1 = InlineKeyboardButton(f'Wildberris', callback_data='market_place')  # изменить параметр кол бек дата
        item2 = InlineKeyboardButton('Ссылка', callback_data='link')
        item3 = InlineKeyboardButton('Желаемая цена', callback_data='wanna_price')
        item4 = InlineKeyboardButton('Верхняя цена', callback_data='high_price')
        keyboard.add(item1, item2, item3, item4)
        bot.send_message(chat_id, 'Добавление товара', reply_markup=keyboard)
        bot.send_message(chat_id, 'Пришлите ссылку⬇')
        bot.answer_callback_query(call.id, f'Пришлите ссылку')
        session = Session(bind=engine)

        user = session.query(Data).filter_by(user_id=chat_id).first()
        if user:
            user.market_place = 'Wildberries'
            session.commit()

        # bot.delete_message(call.message.chat.id, call.message.message_id)
        # bot.delete_message(call.message.chat.id, call.message.message_id + 1)
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
        # bot.delete_message(call.message.chat.id, call.message.message_id)


bot.infinity_polling()
