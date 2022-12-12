import telebot
import conf
from conf import TOKEN
from telebot import types
from string import Template
import time

bot = telebot.TeleBot(TOKEN)

user_dict = {}


class User:
    def __init__(self, city):
        self.city = city

        keys = ['fullname', 'phone', 'supervisor', 'deliveryAdress', 'choice', 'next', 'orderDate', 'photo',
                'date_depart', 'date_arive', 'accommodation', 'wish']

        for key in keys:
            self.key = None


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton('Оформити відрядження')
    item2 = types.KeyboardButton('Як користуватись ботом?')
    item3 = types.KeyboardButton("Телефон для зав'язку з менеджером")
    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id,
                     'Вітаємо вас у чат-боті швидкого оформлення відрядження!'
                     .format(message.from_user),
                     reply_markup=markup)


# @bot.message_handler(content_types=['text'])
# def send_sms(message):
#     if message.chat.type == 'private':
#         if message.text == 'Як користуватись ботом?':
#             bot.send_message(message.chat.id, '1) Поступово відповідайте на питання які буде присилати бот \n'
#                                               '2) Не завантажуйте фото, відео, документи \n')
#         if message.text == "Телефон для зав'язку з менеджером":
#             bot.send_message(message.chat.id, 'Тут будет номер телефона')
#         else:

@bot.message_handler(content_types=['text'])
def user_reg(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Київ')
    itembtn2 = types.KeyboardButton('Одеса')
    itembtn3 = types.KeyboardButton('Дніпро')
    itembtn4 = types.KeyboardButton('Харків')
    itembtn5 = types.KeyboardButton('Львів')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)

    msg = bot.send_message(message.chat.id, 'Оберіть ваше місто', reply_markup=markup)
    bot.register_next_step_handler(msg, process_city_step)


def process_city_step(message):
    try:
        chat_id = message.chat.id
        user_dict[chat_id] = User(message.text)

        markup = types.ReplyKeyboardRemove(selective=False)

        msg = bot.send_message(chat_id, "Вкажіть ваше Прізвище та Імя", reply_markup=markup)
        bot.register_next_step_handler(msg, process_fullname_step)

    except Exception as e:
        bot.reply_to(message,
                     f'Щось пішло не так!\n Якщо далі бот не реагує на повідомлення, пропишіть команду "/start"')


def process_fullname_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.fullname = message.text

        msg = bot.send_message(chat_id, 'Вкажіть ваш номер телефону')
        bot.register_next_step_handler(msg, process_date_depart_step)
    except Exception as e:
        bot.reply_to(message,
                     f'Щось пішло не так!\n Якщо далі бот не реагує на повідомлення, пропишіть команду "/start"')


def process_date_depart_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.phone = message.text

        msg = bot.send_message(chat_id, 'Вкажіть дату відправлення та бажаний час')
        bot.register_next_step_handler(msg, process_date_arrive_step)
    except Exception as e:
        bot.reply_to(message,
                     f'Щось пішло не так!\n Якщо далі бот не реагує на повідомлення, пропишіть команду "/start"')


def process_date_arrive_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.date_depart = message.text

        msg = bot.send_message(chat_id, 'Вкажіть дату повернення та бажаний час')
        bot.register_next_step_handler(msg, process_phone_step)
    except Exception as e:
        bot.reply_to(message,
                     f'Щось пішло не так!\n Якщо далі бот не реагує на повідомлення, пропишіть команду "/start"')


def process_phone_step(message):
    try:

        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.date_arive = message.text

        msg = bot.send_message(chat_id, 'Вкажіть свого керівника, який буде відповідати за заявку')
        bot.register_next_step_handler(msg, process_supervisor_step)
    except Exception as e:
        bot.reply_to(message,
                     f'Щось пішло не так!\n Якщо далі бот не реагує на повідомлення, пропишіть команду "/start"')


def process_supervisor_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.supervisor = message.text

        msg = bot.send_message(chat_id, 'Вкажіть пункт призначення')
        bot.register_next_step_handler(msg, next_step)
    except Exception as e:
        bot.reply_to(message,
                     f'Щось пішло не так!\n Якщо далі бот не реагує на повідомлення, пропишіть команду "/start"')


def next_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.deliveryAdress = message.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        itembtn1 = types.KeyboardButton('Так')
        itembtn2 = types.KeyboardButton('Ні')

        markup.add(itembtn1, itembtn2)

        msg = bot.send_message(message.chat.id, 'Потрібно купляти білети?', reply_markup=markup)
        bot.register_next_step_handler(msg, choice)
    except Exception as e:
        bot.reply_to(message,
                     f'Щось пішло не так!\n Якщо далі бот не реагує на повідомлення, пропишіть команду "/start"')


def choice(message):
    try:
        if message.chat.type == 'private':
            if message.text == 'Так':
                chat_id = message.chat.id
                user = user_dict[chat_id]
                user.choice = message.text

                msg = bot.send_message(chat_id, 'Напишіть, потяг чи автобус')
                bot.register_next_step_handler(msg, process_accommodation_step)
            else:
                chat_id = message.chat.id
                user = user_dict[chat_id]
                user.choice = message.text

                msg = bot.send_message(message.chat.id, 'Особисте авто чи службове? '
                                                        '(Якщо особисте, вкажіть розхід палива на 100км)')
                bot.register_next_step_handler(msg, process_accommodation_step)

    except Exception as e:
        bot.reply_to(message,
                     f'Щось пішло не так!\n Якщо далі бот не реагує на повідомлення, пропишіть команду "/start"')


def process_accommodation_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.orderDate = message.text

        msg = bot.send_message(chat_id, 'Чи потрібно вам бронювати житло? Якщо так, вкажіть, квартиру чи готель. ')
        bot.register_next_step_handler(msg, process_wish_step)
    except Exception as e:
        bot.reply_to(message,
                     f'Щось пішло не так!\n Якщо далі бот не реагує на повідомлення, пропишіть команду "/start"')


def process_wish_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.accommodation = message.text

        msg = bot.send_message(chat_id, 'Якщо у вас є побажання, вкажіть їх тут')
        bot.register_next_step_handler(msg, process_orderDate_step)

    except Exception as e:
        bot.reply_to(message,
                     f'Щось пішло не так!\n Якщо далі бот не реагує на повідомлення, пропишіть команду "/start"')


def process_orderDate_step(message):
    # try:
    chat_id = message.chat.id
    user = user_dict[chat_id]
    user.wish = message.text
    # Ваша заявка
    bot.send_message(chat_id, getRegData(user, 'Ваша заявка',
                                         message.from_user.first_name + "\nУ Випадку неточностей, з вами зв'яжеться менеджер з відряджень"),
                     parse_mode='Markdown')
    # Отправить в группу
    bot.send_message(conf.CHANNEL_ID, getRegData(user, 'Заявка от бота', bot.get_me().username),
                     parse_mode='Markdown')


def getRegData(user, title, name):
    t = Template('$title *$name* \n Місто: *$userCity* \n ПІБ: *$fullname* \n Номер телефону: *$phone* \n '
                 'Керівник: *$supervisor* \n Місце прибуття: *$deliveryAdress* \n Тип транспорту: *$orderDate* \n '
                 'Дата відправлення: *$date_depart* \n Дата повернення: *$date_arive* \n Житло: *$accommodation* \n '
                 'Побажання: *$wish*')

    return t.substitute({
        'title': title,
        'name': name,
        'userCity': user.city,
        'fullname': user.fullname,
        'phone': user.phone,
        'supervisor': user.supervisor,
        'deliveryAdress': user.deliveryAdress,
        'orderDate': user.orderDate,
        'date_depart': user.date_depart,
        'date_arive': user.date_arive,
        'accommodation': user.accommodation,
        'wish': user.wish

    })


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

if __name__ == '__main__':  # чтобы код выполнялся только при запуске в виде сценария, а не при импорте модуля
    try:
        bot.polling(none_stop=True)  # запуск бота
    except Exception as e:
        print(e)  # или import traceback; traceback.print_exc() для печати полной инфы
        time.sleep(15)
