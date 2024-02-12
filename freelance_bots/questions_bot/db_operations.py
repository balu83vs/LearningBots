from db_create import db_connect
from datetime import datetime


# внесение новых пользователей в БД
def new_user_creating(user_id, company_id = 0, team_id = 0, admin = 0):
    conn, cursor = db_connect() # подключение к базе данных SQLite
    # выборка пользователя с определенным user_id
    sql = "select * from users where user_id=:user_id"
    cursor.execute(sql, {"user_id": user_id})

    # проверка наличия пользователя в базе
    # пользователь есть в базе
    if cursor.fetchone():                       
        conn.close()  # завершение сеанса БД
        return False
    
    # пользователя нет в базе 
    else:                                       
        # внесение в таблицу users записи о пользователе 
        cursor.execute('''
            INSERT INTO users (user_id, company_id, team_id, admin)
            VALUES (?, ?, ?, ?)
        ''', (user_id, company_id, team_id, admin))
        conn.commit() # внесение изменений в БД
        conn.close()
        return True


# получение списка пользователей команды из БД
def get_team_users(team_id):
    conn, cursor = db_connect()
    # выборка всех пользователей из базы
    sql = "select user_id from users where team_id=:team_id"
    cursor.execute(sql, {"team_id": team_id})
    users = cursor.fetchall()
    conn.close()    
    return users


# проверка административных прав
def check_admin_permissions(user_id):
    conn, cursor = db_connect()
    # выборка пользователей с определенным user_id и статусом admin 
    sql = "select * from users where user_id=:user_id and admin=:admin"
    cursor.execute(sql, {"user_id": user_id, "admin": 1})
    admin = cursor.fetchall()
    conn.close()
    return admin        


# сохранение вопроса в БД
def save_question(data):
    conn, cursor = db_connect()
    date = datetime.now() # присваиваем переменной текущую дату
    # внесение записи о вопросе в таблицу questions
    cursor.execute('''
        INSERT OR REPLACE INTO questions (title, date, team_id, type)
        VALUES (?, ?, ?, ?)
    ''', (data.get('question'), date, data.get('team_id'), data.get('type')))
    conn.commit()   
    

# загрузка вопроса из БД
def get_question():
    conn, cursor = db_connect()
    # выборка всех вопросов из базы
    """
    sql = "select * from questions where id=:question_id"
    cursor.execute(sql, {"question_id": question_id})
    """
    # выборка из базы вопроса с максимальным id
    sql = "select id, title, type from questions where id=(SELECT MAX(id) FROM questions)"
    cursor.execute(sql)
    questions = cursor.fetchall()
    conn.close()    
    return questions


# удаление вопроса из БД
def del_question(question_id):
    conn, cursor = db_connect()
    # удаление определенного вопроса из таблицы questions
    sql = "DELETE FROM questions WHERE id=:question_id"
    cursor.execute(sql, {"question_id": question_id})
    conn.commit()


# сохранение ответа в БД
def save_answer(question_id, answer, user_id):
    conn, cursor = db_connect()
    date = datetime.now()
    # внесение записи об ответе в таблицу answers
    cursor.execute('''
        INSERT OR REPLACE INTO answers (question_id, date, answer_title, user_id)
        VALUES (?, ?, ?, ?)
    ''', (question_id, date, answer, user_id))
    conn.commit()


# сохранение сообщения в БД
def save_message(data, admin_id):
    conn, cursor = db_connect()
    date = datetime.now()
    # внесение записи о сообщении в таблицу messages
    cursor.execute('''
        INSERT OR REPLACE INTO messages (title, date, team_id, admin_id)
        VALUES (?, ?, ?, ?)
    ''', (data.get('text_message'), date, data.get('team_id'), admin_id))
    conn.commit()


# загрузка сообщения из БД
def get_message():
    conn, cursor = db_connect()
    # выборка всех сообщений из базы
    #sql = "select * from messages where id=:message_id"
    #cursor.execute(sql, {"message_id": message_id})
    # выборка из базы сообщения с максимальным id
    sql = "select id, title from messages where id=(SELECT MAX(id) FROM messages)"
    cursor.execute(sql)
    messages = cursor.fetchall()
    conn.close()    
    return messages    