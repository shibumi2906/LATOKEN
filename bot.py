from loguru import logger
import telebot
import openai
import sqlite3
import os
# Укажите свои ключи API
TELEGRAM_API_KEY = 'ваш телеграмм токен'
OPENAI_API_KEY = 'ВАШ ТОКЕН'

# Проверка наличия ключей
if not TELEGRAM_API_KEY or not OPENAI_API_KEY:
    logger.error("Отсутствуют необходимые ключи API.")
    raise ValueError("Отсутствуют TELEGRAM_API_KEY или OPENAI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_API_KEY)
openai.api_key = OPENAI_API_KEY

user_context = {}

def get_db_connection():
    conn = sqlite3.connect('quiz_answers.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_random_question():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT question, answer FROM answers ORDER BY RANDOM() LIMIT 1")
        return cursor.fetchone()

def get_openai_response(user_id, prompt, db_answer=None):
    user_data = user_context.get(user_id, {})
    messages = user_data.get("messages", [])

    if not isinstance(messages, list):
        messages = []

    if not messages:
        messages.append({
            "role": "system",
            "content": (
                "Ты действуешь как опытный сотрудник LATOKEN, который представляет "
                "свою любимую фирму потенциальным инвесторам и сотрудникам."
                "Если тебе задают вопросы не относящиеся к твоей фирме, то нужно мягко, с юмором , вернуть беседу к теме LATOKEN"
                "После 4 вопросов, говоришь , что теперь твоя очередь задавать вопросы.Если пользователь говорит , что у него больше нет вопросов или предлагает начать задавать вопросы ему ты начинаешь задавать вопросы о LATOKEN."
            )
        })

    if db_answer:
        messages.append({
            "role": "assistant",
            "content": f"На основе базы данных: {db_answer}"
        })

    messages.append({"role": "user", "content": prompt})
    logger.info(f"Получен запрос от пользователя {user_id}: {prompt}")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages
        )
        assistant_message = response['choices'][0]['message']['content']
        logger.info(f"Ответ от OpenAI для пользователя {user_id}: {assistant_message}")
    except Exception as e:
        assistant_message = "Произошла ошибка при обращении к OpenAI. Попробуйте позже."
        logger.error(f"Ошибка при запросе к OpenAI для пользователя {user_id}: {e}")

    messages.append({"role": "assistant", "content": assistant_message})
    user_data["messages"] = messages
    user_context[user_id] = user_data

    return assistant_message

@bot.message_handler(commands=['start'])
def start_conversation(message):
    user_context[message.chat.id] = {
        "initialized": True,
        "messages": []
    }

    welcome_message = (
        "Здравствуйте! Я нейро-сотрудник компании LATOKEN. "
        "Моя задача — ответить на ваши вопросы о компании, "
        "а затем мы поменяемся местами, и я задам вам несколько вопросов. "
        "Начинаем!"
    )
    bot.send_message(message.chat.id, welcome_message)

@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    user_data = user_context.get(message.chat.id)

    if not user_data or not user_data.get("initialized"):
        bot.send_message(message.chat.id, "Пожалуйста, начните с команды /start.")
        return

    user_question = message.text.strip()

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT answer FROM answers WHERE question = ?", (user_question,))
        db_answer = cursor.fetchone()

    db_answer = db_answer[0] if db_answer else None
    response = get_openai_response(message.chat.id, user_question, db_answer)

    bot.send_message(message.chat.id, response)

if __name__ == '__main__':
    logger.info("Запуск бота...")
    bot.polling(none_stop=True, interval=1, timeout=20)

