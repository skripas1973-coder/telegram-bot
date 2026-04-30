import telebot
import os
import requests
import time

TOKEN = os.getenv("TOKEN")
AI_KEY = os.getenv("AI_KEY")

bot = telebot.TeleBot(TOKEN)

def ask_ai(prompt):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {AI_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistralai/mistral-7b-instruct",  # ✅ бесплатная модель
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )

    data = response.json()

    if "choices" in data:
        return data["choices"][0]["message"]["content"]
    else:
        return f"❌ Ошибка:\n{data}"

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

    ai2 = ask_ai(f"Ответь на это сообщение:\n{ai1}")
    bot.send_message(chat_id, f"🧠 Бот 2:\n{ai2}")

    time.sleep(2)

    ai3 = ask_ai(f"Ответь на это:\n{ai2}")
    bot.send_message(chat_id, f"🤖 Бот 1:\n{ai3}")

    time.sleep(2)

    ai4 = ask_ai(f"Ответь на это:\n{ai3}")
    bot.send_message(chat_id, f"🧠 Бот 2:\n{ai4}")

print("✅ Бот с ИИ запущен")
bot.infinity_polling()
