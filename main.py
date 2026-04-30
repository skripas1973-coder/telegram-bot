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

# Получение access token от GigaChat
def get_access_token():
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": "123456"
    }

    data = {
        "scope": "GIGACHAT_API_PERS"
    }

    response = requests.post(
        url,
        headers=headers,
        data=data,
        auth=("api-key", GIGA_KEY),
        verify=False
    )

    return response.json()["access_token"]


# Запрос к ИИ
def ask_giga(prompt, token):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "GigaChat",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data, verify=False)

    result = response.json()

    if "choices" in result:
        return result["choices"][0]["message"]["content"]
    else:
        return f"❌ Ошибка:\n{result}"


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🤖 Два ИИ начинают диалог...\nНапиши тему")


@bot.message_handler(func=lambda message: True)
def chat(message):
    topic = message.text

    bot.send_message(message.chat.id, "🧠 ИИ думают...")

    token = get_access_token()

    msg = topic

    for i in range(4):
        answer1 = ask_giga(msg, token)
        bot.send_message(message.chat.id, f"🤖 Бот 1:\n{answer1}")

        time.sleep(2)

        answer2 = ask_giga(answer1, token)
        bot.send_message(message.chat.id, f"🧠 Бот 2:\n{answer2}")

        time.sleep(2)

        msg = answer2


print("Бот запущен...")
bot.infinity_polling()
