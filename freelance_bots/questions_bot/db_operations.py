from db_create import db_connect


# функция для получения списка пользователей из базы данных
def get_users_from_database():
    pass

# функция для получения вопроса из базы данных
def get_question_from_database():
    pass

# функция для получения текущего вопроса пользователя
def get_current_question_id():
    pass

# функция для получения следующего вопроса
def get_next_question():
    pass

# функция сохранения ответа в БД
def save_answer(user_id, question_id, answer):

    # Подключение к базе данных SQLite
    conn, cursor = db_connect()

    # 
    cursor.execute('''
        INSERT OR REPLACE INTO answers (user_id, question_id, answer)
        VALUES (?, ?, ?)
    ''', (user_id, question_id, answer))
    conn.commit()
