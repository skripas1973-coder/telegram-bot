import telebot
import os
import requests
import time

TOKEN = os.getenv("TOKEN")
GIGA_KEY = os.getenv("GIGA_KEY")

if TOKEN is None or GIGA_KEY is None:
    print("❌ Нет TOKEN или GIGA_KEY")
    exit()

bot = telebot.TeleBot(TOKEN)

# Получение токена
def get_access_token():
    try:
        response = requests.post(
            "https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
                "RqUID": "123456"
            },
            data={"scope": "GIGACHAT_API_PERS"},
            auth=("api-key", GIGA_KEY),
            timeout=10
        )
        return response.json()["access_token"]
    except Exception as e:
        return None


# Запрос к ИИ
def ask_giga(prompt, token):
    try:
        response = requests.post(
            "https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json={
                "model": "GigaChat",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            },
            timeout=15
        )

        data = response.json()

        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        else:
            return f"❌ Ошибка:\n{data}"

    except Exception as e:
        return f"❌ Ошибка запроса: {e}"


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🤖 Два ИИ начинают диалог...\nНапиши тему")


@bot.message_handler(func=lambda message: True)
def chat(message):
    chat_id = message.chat.id
    topic = message.text

    bot.send_message(chat_id, "🧠 ИИ думают...")

    token = get_access_token()

    if token is None:
        bot.send_message(chat_id, "❌ Не удалось получить токен GigaChat")
        return

    msg = topic

    for i in range(3):
        answer1 = ask_giga(msg, token)
        bot.send_message(chat_id, f"🤖 Бот 1:\n{answer1}")

        time.sleep(1.5)

        answer2 = ask_giga(answer1, token)
        bot.send_message(chat_id, f"🧠 Бот 2:\n{answer2}")

        time.sleep(1.5)

        msg = answer2


print("Бот запущен...")
bot.infinity_polling()
