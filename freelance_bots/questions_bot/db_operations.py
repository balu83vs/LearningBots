from db_create import db_connect

from datetime import datetime

# функция первоначального внесения пользователей в базу данных
def new_user_creating(user_id, company_id = 0, team_id = 0, admin = 0):
    # Подключение к базе данных SQLite
    conn, cursor = db_connect()
    # проверка наличия пользователя в базе
    sql = "select * from users where user_id=:user_id"
    cursor.execute(sql, {"user_id": user_id})

    if cursor.fetchone():
        conn.close()
        return False
    else:
        # внесение записи о пользователе в базу users 
        cursor.execute('''
            INSERT INTO users (user_id, company_id, team_id, admin)
            VALUES (?, ?, ?, ?)
        ''', (user_id, company_id, team_id, admin))

        conn.commit()
        conn.close()
        return True

# проверка административных прав
def check_admin_permissions(user_id):
    # Подключение к базе данных SQLite
    conn, cursor = db_connect()
    sql = "select * from users where user_id=:user_id and admin=:admin"
    cursor.execute(sql, {"user_id": user_id, "admin": 1})
    admin = cursor.fetchall()
    conn.close()
    return admin        

# функция для получения списка пользователей из базы данных
def get_users_from_database():
    # Подключение к базе данных SQLite
    conn, cursor = db_connect()
    # выборка всех пользователей из базы
    sql = "select user_id from users"
    cursor.execute(sql)
    users = cursor.fetchall()
    conn.close()    
    return users

# функция для получения вопроса из базы данных
def get_question_from_database():
    pass

# функция для получения текущего вопроса пользователя
def get_current_question_id():
    pass

# функция для получения следующего вопроса
def get_next_question():
    pass

# функция сохранения вопроса в БД
def save_question(data):
    # Подключение к базе данных SQLite
    conn, cursor = db_connect()
    date = datetime.now()
    # внесение записи о вопросе в базу questions
    cursor.execute('''
        INSERT OR REPLACE INTO questions (title, date, team_id, type)
        VALUES (?, ?, ?, ?)
    ''', (data.get('question'), date, data.get('team_id'), data.get('type')))
    try: 
        conn.commit()
        return True
    except:
        return False

# функция сохранения ответа в БД
def save_answer(question_id, answer):
    # Подключение к базе данных SQLite
    conn, cursor = db_connect()
    date = datetime.now()
    # внесение записи об ответе в базу questions
    cursor.execute('''
        INSERT OR REPLACE INTO answers (question_id, date, answer)
        VALUES (?, ?, ?)
    ''', (question_id, date, answer))
    conn.commit()
