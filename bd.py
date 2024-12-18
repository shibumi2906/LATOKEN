import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('quiz_answers.db')
cursor = conn.cursor()

# Создание таблицы, если она не существует
cursor.execute('''
CREATE TABLE IF NOT EXISTS answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
)
''')

# Данные для вставки
data = [
    (
        "Почему LATOKEN помогает людям изучать и покупать активы?",
        "LATOKEN стремится сделать деньги доступными для людей, чтобы они могли строить и совместно владеть будущим. Компания предоставляет платформу, упрощающую доступ к различным активам и обучению, что соответствует их миссии."
    ),
    (
        "Зачем нужен Sugar Cookie тест?",
        "Sugar Cookie тест используется для оценки решимости и выносливости кандидатов. Он помогает определить, способны ли они преодолевать трудности и сохранять мотивацию в сложных ситуациях, что соответствует культуре LATOKEN."
    ),
    (
        "Зачем нужен Wartime CEO?",
        "Концепция Wartime CEO относится к лидеру, который эффективно управляет компанией в условиях кризиса или высокой конкуренции. Такие руководители принимают быстрые и решительные решения, фокусируются на приоритетах и способны адаптироваться к быстро меняющимся обстоятельствам."
    ),
    (
        "В каких случаях стресс полезен и в каких вреден?",
        "Стресс может быть полезен в краткосрочной перспективе, когда он мобилизует ресурсы организма для преодоления вызовов и достижения целей. Однако длительный или хронический стресс вреден, так как он может привести к выгоранию, снижению продуктивности и негативно сказаться на здоровье. В культуре LATOKEN подчеркивается важность умения управлять стрессом, чтобы поддерживать высокую эффективность и благополучие сотрудников."
    )
]

# Вставка данных в таблицу
cursor.executemany("INSERT INTO answers (question, answer) VALUES (?, ?)", data)

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print("База данных успешно дополнена.")




