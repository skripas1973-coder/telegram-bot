import telebot
import os
import requests
import time

TOKEN = os.getenv("TOKEN")
AI_KEY = os.getenv("AI_KEY")

if TOKEN is None or AI_KEY is None:
    print("❌ Нет TOKEN или AI_KEY")
    exit()

bot = telebot.TeleBot(TOKEN)

def ask_ai(prompt):
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {AI_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "meta-llama/llama-3-8b-instruct:free",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )

        data = response.json()

        if "error" in data:
            return f"❌ Ошибка:\n{data}"

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ Ошибка: {e}"


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🤖 Два ИИ начинают диалог...\nНапиши тему")


@bot.message_handler(func=lambda message: True)
def chat(message):
    topic = message.text

    bot.send_message(message.chat.id, "🧠 ИИ думают...")

    msg = topic

    for i in range(4):
        answer1 = ask_ai(msg)
        bot.send_message(message.chat.id, f"🤖 Бот 1:\n{answer1}")

        time.sleep(2)

        answer2 = ask_ai(answer1)
        bot.send_message(message.chat.id, f"🧠 Бот 2:\n{answer2}")

        time.sleep(2)

        msg = answer2


print("Бот запущен...")
bot.infinity_polling()
