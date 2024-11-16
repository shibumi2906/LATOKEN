import sqlite3

# Подключение к базе данных
db_path = 'quiz_bot.db'  # Укажите путь к вашей базе данных
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Получение списка таблиц
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Вывод списка таблиц
print("Список таблиц в базе данных:")
for table in tables:
    print(table[0])

conn.close()

