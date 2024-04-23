from db_con import DbSqlConnector


sql_db = DbSqlConnector()


def data_input(query):
    sql_db.open_connection()
    sql_db.add_query(query)
    sql_db.close_connection()


def data_output(query):
    sql_db.open_connection()
    data = sql_db.out_query(query)
    sql_db.close_connection()
    return data