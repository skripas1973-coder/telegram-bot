import telebot
import requests
import time
import os

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)

def ask_ai(prompt):
    try:
        response = requests.post(
            "https://api.affiliateplus.xyz/api/chatbot",
            json={
                "message": prompt,
                "botname": "Bot",
                "ownername": "User"
            }
        )

        data = response.json()
        return data["message"]

    except:
        return "Ошибка ИИ 😢"

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🤖 Два ИИ начинают диалог...\nНапиши тему")

@bot.message_handler(func=lambda message: True)
def dialogue(message):
    chat_id = message.chat.id
    topic = message.text

    bot.send_message(chat_id, "🧠 ИИ думают...")

    ai1 = ask_ai(f"Начни разговор на тему: {topic}")
    bot.send_message(chat_id, f"🤖 Бот 1:\n{ai1}")

    time.sleep(2)

    ai2 = ask_ai(ai1)
    bot.send_message(chat_id, f"🧠 Бот 2:\n{ai2}")

    time.sleep(2)

    ai3 = ask_ai(ai2)
    bot.send_message(chat_id, f"🤖 Бот 1:\n{ai3}")

    time.sleep(2)

    ai4 = ask_ai(ai3)
    bot.send_message(chat_id, f"🧠 Бот 2:\n{ai4}")

print("✅ Бесплатный ИИ бот запущен")
bot.infinity_polling()
