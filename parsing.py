import requests
from bs4 import BeautifulSoup
import sqlite3

# URLs для парсинга
urls = [
    "https://coda.io/@latoken/latoken-talent/culture-139",
    "https://deliver.latoken.com/hackathon"
]

# Подключение к базе данных
def get_db_connection():
    conn = sqlite3.connect('quiz_bot.db')
    return conn

# Парсинг страницы
def parse_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text(separator="\n")
        return text.strip()
    else:
        return None

# Обновление базы данных
def update_database(url, content):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Проверяем, есть ли запись с этим URL
    cursor.execute("SELECT id FROM information WHERE url = ?", (url,))
    existing = cursor.fetchone()
    if existing:
        # Обновляем запись
        cursor.execute("UPDATE information SET content = ? WHERE url = ?", (content, url))
        print(f"Обновлено содержимое для {url}")
    else:
        # Добавляем новую запись
        cursor.execute("INSERT INTO information (url, content) VALUES (?, ?)", (url, content))
        print(f"Добавлено содержимое для {url}")
    conn.commit()
    conn.close()

# Основной парсер
def main():
    for url in urls:
        print(f"Парсинг {url}...")
        content = parse_page(url)
        if content:
            update_database(url, content)
        else:
            print(f"Ошибка при парсинге {url}")

if __name__ == "__main__":
    main()

