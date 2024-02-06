from db_create import db_connect
from datetime import datetime


# внесение новых пользователей в БД
def new_user_creating(user_id, company_id = 0, team_id = 0, admin = 0):
    # Подключение к базе данных SQLite и выборка пользователя с определенным user_id
    conn, cursor = db_connect()
    sql = "select * from users where user_id=:user_id"
    cursor.execute(sql, {"user_id": user_id})

    # проверка наличия пользователя в базе
    if cursor.fetchone():                       # пользователь есть в базе
        # завершение сеанса БД
        conn.close()
        return False
    else:                                       # пользователя нет в базе 
        # внесение записи о пользователе в базу users
        cursor.execute('''
            INSERT INTO users (user_id, company_id, team_id, admin)
            VALUES (?, ?, ?, ?)
        ''', (user_id, company_id, team_id, admin))

        conn.commit()
        # завершение сеанса БД
        conn.close()
        return True


# получение списка пользователей из БД
def get_users(team_id):
    # Подключение к базе данных SQLite
    conn, cursor = db_connect()
    # выборка всех пользователей из базы
    sql = "select user_id from users where team_id=:team_id"
    cursor.execute(sql, {"team_id": team_id})
    users = cursor.fetchall()
    conn.close()    
    return users


# проверка административных прав
def check_admin_permissions(user_id):
    # Подключение к базе данных SQLite
    conn, cursor = db_connect()
    sql = "select * from users where user_id=:user_id and admin=:admin"
    cursor.execute(sql, {"user_id": user_id, "admin": 1})
    admin = cursor.fetchall()
    conn.close()
    return admin        


# сохранение вопроса в БД
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
    

# загрузка вопроса из БД
def get_question():
    # Подключение к базе данных SQLite
    conn, cursor = db_connect()
    # выборка всех вопросов из базы
    #sql = "select * from questions where id=:question_id"
    #cursor.execute(sql, {"question_id": question_id})
    sql = "select id, title, type from questions where id=(SELECT MAX(id) FROM questions)"
    cursor.execute(sql)
    questions = cursor.fetchall()
    conn.close()    
    return questions


# удаление вопроса из БД
def del_question(question_id):
    # Подключение к базе данных SQLite
    conn, cursor = db_connect()
    # удаление вопроса из бд questions
    sql = "DELETE FROM questions WHERE id=:question_id"
    cursor.execute(sql, {"question_id": question_id})
    conn.commit()


# сохранение ответа в БД
def save_answer(question_id, answer):
    # Подключение к базе данных SQLite
    conn, cursor = db_connect()
    date = datetime.now()
    # внесение записи об ответе в базу questions
    cursor.execute('''
        INSERT OR REPLACE INTO answers (question_id, date, answer_title)
        VALUES (?, ?, ?)
    ''', (question_id, date, answer))
    conn.commit()


# сохранение сообщения в БД
def save_message(data):
    # Подключение к базе данных SQLite
    conn, cursor = db_connect()
    date = datetime.now()
    # внесение записи о сообщении в базу messages
    cursor.execute('''
        INSERT OR REPLACE INTO messages (title, date, team_id)
        VALUES (?, ?, ?)
    ''', (data.get('text_message'), date, data.get('team_id')))
    conn.commit()


# загрузка сообщения из БД
def get_message():
    # Подключение к базе данных SQLite
    conn, cursor = db_connect()
    # выборка всех сообщений из базы
    #sql = "select * from messages where id=:message_id"
    #cursor.execute(sql, {"message_id": message_id})
    sql = "select id, title from messages where id=(SELECT MAX(id) FROM messages)"
    cursor.execute(sql)
    messages = cursor.fetchall()
    conn.close()    
    return messages    