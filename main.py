import telebot
import os

# Берём токен из Railway
TOKEN = os.getenv("TOKEN")

# Проверка
if TOKEN is None:
    print("❌ TOKEN не найден!")
    exit()

bot = telebot.TeleBot(TOKEN)

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Бот работает 🚀")

# Ответ на любые сообщения
@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.send_message(message.chat.id, "Ты написал: " + message.text)

print("Бот запущен...")

bot.infinity_polling()
