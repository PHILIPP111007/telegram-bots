import time
import requests

# My module that contains TOKEN
import config

# pyTelegramBotAPI
import telebot
from telebot import types


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start(message):

	response = f"""
Hello!\n
I am phil_bot
You are <b>{message.from_user.username}</b>
Your first name: <b>{message.from_user.first_name}</b>
Your last name: <b>{message.from_user.last_name}</b>

What can this bot do?

-- if you sent a number, you will get <i>interesting information</i> about it
-- see also <i>list of commands</i>
"""

	bot.send_message(message.chat.id, response, parse_mode='HTML')


@bot.message_handler(commands=['timer'])
def set_time(message):
	bot.send_message(message.chat.id, 'Enter number of seconds:')
	bot.register_next_step_handler(message, set_timer)


@bot.message_handler(commands=["get_user_data"])
def get_user_data(message):
	bot.send_message(message.chat.id, message.from_user)



def set_timer(message):
	try:
		sec = int(message.text)
		if 300 >= sec >= 0:
			kb = types.InlineKeyboardMarkup(row_width=1)
			btn = types.InlineKeyboardButton(text='Start', callback_data=str(sec))
			kb.add(btn)
			bot.send_message(message.chat.id, f'Timer for <b>{sec}</b> seconds', reply_markup=kb, parse_mode='HTML')
		else:
			bot.send_message(message.chat.id, 'The number is too big, I will get tired of counting😞\nTry less than 300')
	except Exception:
		pass


@bot.callback_query_handler(func=lambda callback: True)
def timer_buttons(callback):
	if callback.data:
		sec = int(callback.data)
		bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=f'Timer for {sec} seconds')

		run_timer(message=callback.message, sec=int(sec))


def run_timer(message, sec):

	if sec == 0:
		bot.send_message(message.chat.id, '⏰')
	elif 300 >= sec >= 1:
		messagetoedit = bot.send_message(message.chat.id, f'Time left: {sec}⏳')
		time.sleep(1)
		if sec > 1:
			for i in range(sec - 1, 0, -1):
				bot.edit_message_text(chat_id=message.chat.id, message_id=messagetoedit.message_id, text=f'Time left: {i}⏳')
				time.sleep(1)
		bot.delete_message(message.chat.id, messagetoedit.message_id)
		bot.send_message(message.chat.id, '⏰')


@bot.message_handler(regexp=r'[0-9]+')
def get_info_about_number(message):
	r = requests.get(f'http://numbersapi.com/{message.text}')
	bot.send_message(message.chat.id, r)


if __name__ == '__main__':
	bot.skip_pending = True
	bot.infinity_polling()
