import telebot

bot = telebot.TeleBot("6972868806:AAHUtfGbzbcryr7D6RZLOUD9CMg7FO8Csxk")
@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'Привет!')

bot.polling(none_stop=True)