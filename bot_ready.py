import telebot 
import config

bot = telebot.TeleBot(config.API)

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}!')

bot.infinity_polling()