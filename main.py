import telebot
import os

# Берём токен из Railway
TOKEN = os.getenv("TOKEN")

# Проверка (чтобы не падал молча)
if TOKEN is None:
    print("❌ TOKEN не найден!")
    exit()

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Бот работает 🚀")

print("Бот запущен...")

bot.infinity_polling()
