import sqlite3
from config import db_name


# функция подключения к базе данных SQLite
def db_connect():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    return conn, cursor


# функция создания БД
def db_create():

    # Подключение к базе данных SQLite
    conn, cursor = db_connect()

    # Создание таблицы для пользователей
    """
    Таблица users. 
    Поля: id(PK), user_id (телеграм id), company_id(FK), team_id(FK), admin(boolean)
    """
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            company_id INTEGER,
            team_id INTEGER,
            admin BOOLEAN DEFAULT (0),
            FOREIGN KEY (company_id)
            REFERENCES companies (id) ON DELETE CASCADE
            FOREIGN KEY (team_id)
            REFERENCES teams (id) ON DELETE CASCADE          
        )
    ''')

    # Создание таблицы для компаний
    """
    Таблица companies. 
    Поля: id(PK), title (уникальное)
    """
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(200) UNIQUE
        )
    ''')
    
    # Создание таблицы для команд
    """
    Таблица teams. 
    Поля: id(PK), title(уникальное), company_id(FK)
    """
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(200) UNIQUE,
            company_id INTEGER,
            FOREIGN KEY (company_id)     
            REFERENCES companies (id) ON DELETE CASCADE     
        )
    ''')
    
    # Создание таблицы для вопросов
    """
    Таблица questions. 
    Поля: id(PK), title(НЕ уникальное поле), date (дата записи в таблицу), 
    tean_id(FK), type (может быть двух типов - 1, 2)
    """
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(200) UNIQUE,
            date DATE,      
            team_id INTEGER, 
            type INTEGER CHECK(type = 1 OR type = 2),       
            FOREIGN KEY (team_id)     
            REFERENCES teams (id) ON DELETE CASCADE     
        )
    ''')

    # Создание таблицы для ответов
    """
    Таблица answers. 
    Поля: id(PK), question_id(FK), date, 
    answer_title (ответы могут быть текстовыми (yes\no) или числовыми (от 1 до 5)), user_id(FK)
    """
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER,       
            date DATE, 
            answer_title VARCHAR(10) CHECK(answer_title IN ('yes', 'no', '1', '2', '3', '4', '5')),   
            user_id INTEGER,       
            FOREIGN KEY (question_id)     
            REFERENCES questions (id) ON DELETE CASCADE   
            FOREIGN KEY (user_id)   
            REFERENCES users (id) ON DELETE CASCADE         
        )
    ''')
    
    # Создание таблицы для сообщений
    """
    Таблица messages. 
    Поля: id(PK), date, title, team_id(FK), admin_id(FK)
    """
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,       
            title VARCHAR(200),  
            team_id INTEGER,     
            admin_id INTEGER,       
            FOREIGN KEY (team_id)            
            REFERENCES teams (id) ON DELETE CASCADE     
            FOREIGN KEY (admin_id)   
            REFERENCES users (id) ON DELETE CASCADE           
        )
    ''')

    conn.commit()
    return cursor