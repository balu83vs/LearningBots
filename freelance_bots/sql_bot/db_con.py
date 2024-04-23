import os

import mysql.connector


USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
DB_NAME = os.getenv("DB_NAME")


class DbSqlConnector:
    """
    Класс взаимодействия с базой данных sql
    """
    def __init__(self, username=USERNAME, password=PASSWORD,
                 host=HOST, db_name=DB_NAME, 
                       ):
        self._username = username
        self._password = password
        self._host = host
        self._db_name = db_name

        self._client = None
    

    # Установка соединения (подключение клиента)
    def open_connection(self):
        """
        Метод устанавливает соединение с базой данных 
        с использованием предоставленных учетных данных.
        """
        self._client = mysql.connector.connect(
            user=self._username, 
            password=self._password,
            host=self._host, 
            database=self._db_name)    


    # Закрытие соединения (отключение клиента)
    def close_connection(self):
        """
        Метод разрывает соединение с базой данных 
        """
        self._client.close()    


    # Запуск указателя
    def add_cursor(self):
        """
        Метод создает курсор для выполнения запросов в базе данных.

        Курсор представляет собой объект, который позволяет выполнять запросы и получать результаты.
        """
        if self._client:
            cursor = self._client.cursor()
            return cursor 
        

    # запрос в БД
    def add_query(self, query):
        """
        Метод выполняет запрос на изменение данных в базе данных, 
        например INSERT, UPDATE или DELETE.
        """

        cursor = self.add_cursor()

        cursor.execute(query)

        self._client.commit()


    # запрос из БД
    def out_query(self, query):
        """
        Метод выполняет запрос на выборку данных из базы данных, например SELECT.
        """
        cursor = self.add_cursor()

        cursor.execute(query)

        data = cursor.fetchall()

        return data