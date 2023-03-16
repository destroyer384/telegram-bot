import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from math import sqrt

with open("start_token.txt", "r") as token:
    bot = telebot.TeleBot(token.readline())


# returns a number, whose square can divide a number evenly
def square_divider(num):
    for i in range(2, int(num // 1))[::-1]:
        if str(num / (i*i)).endswith(".0"):
            return i
    return None


# simplifies square root
def get_square_root(num):
    if str(num).endswith(".0"):
        num = int(num)
    if str(sqrt(num)).endswith(".0"):
        root = int(sqrt(num))
    elif square_divider(num) is not None:
        root = f"{square_divider(num)} * sqrt( {num // (square_divider(num) * square_divider(num))} )"
    else:
        root = f"{round(sqrt(num), 2)}, or sqrt( {num} )"
    return root


# add an unlimited amount of buttons under a message
def inline_buttons(*labels):
    return InlineKeyboardMarkup(row_width=1).add(
        *(InlineKeyboardButton(text=label, callback_data=label) for label in labels))


# triggers if "/start" was sent
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "You're in main menu, choose an option:",
                     reply_markup=inline_buttons(
                         "Get square root",
                         "Get the unknown side"
                     ))


# handler that will consider every callback
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "Get square root":
        bot.send_message(call.message.chat.id, "Enter a number to get square root from")
        bot.register_next_step_handler(call.message, option_1)
    elif call.data == "Get the unknown side":
        bot.send_message(call.message.chat.id, "What sides do you have",
                         reply_markup=inline_buttons(
                             "Two cathetuses",
                             "Cathetus and hypotenuse"
                         ))
    elif call.data == "Two cathetuses":
        bot.send_message(call.message.chat.id, "Enter the values")
        bot.register_next_step_handler(call.message, option_2_1)
    elif call.data == "Cathetus and hypotenuse":
        bot.send_message(call.message.chat.id, "Enter the values")
        bot.register_next_step_handler(call.message, option_2_2)


def option_1(message):
    try:
        num = float(message.text)
        bot.send_message(message.chat.id, f"Square root of {message.text} is {get_square_root(num)}")
        start(message)
    except ValueError:
        bot.send_message(message.chat.id, "Enter a valid number")
        bot.register_next_step_handler(message, option_1)


def option_2_1(message):
    try:
        a, b = map(float, message.text.strip().split())
        bot.send_message(message.chat.id, f"The hypotenuse is {get_square_root((a*a) + (b*b))}")
        start(message)
    except ValueError:
        bot.send_message(message.chat.id, "Enter valid numbers")
        bot.register_next_step_handler(message, option_2_1)


def option_2_2(message):
    try:
        a, c = map(float, message.text.strip().split())
        bot.send_message(message.chat.id, f"The unknown cathetus is {get_square_root(abs((c*c) - (a*a)))}")
        start(message)
    except ValueError:
        bot.send_message(message.chat.id, "Enter valid numbers")
        bot.register_next_step_handler(message, option_2_2)


bot.polling()