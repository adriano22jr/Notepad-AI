import pyodbc, app_config

CONNECTION_STRING = f"Driver={app_config.DB_DRIVER_NAME};Server=tcp:{app_config.DB_SERVER_NAME},1433;Database={app_config.DB_NAME};Uid={app_config.DB_USERNAME};Pwd={app_config.DB_PASSWORD};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

def insert_user(firstname, lastname, email, username):
    connection = pyodbc.connect(CONNECTION_STRING)
    sql_command = f"INSERT INTO [dbo].[Users] (Email, FirstName, LastName, Username) VALUES ('{email}', '{firstname}', '{lastname}', '{username}');"
    connection.execute(sql_command)
    connection.commit()
    connection.close()
    
def delete_user(email):
    connection = pyodbc.connect(CONNECTION_STRING)
    sql_command = f"DELETE FROM [dbo].[Users] WHERE Email = '{email}'"
    connection.execute(sql_command)
    connection.commit()
    connection.close()
    
def check_exising_user(email):
    connection = pyodbc.connect(CONNECTION_STRING)
    sql_command = f"SELECT * FROM [dbo].[Users] WHERE Email = '{email}'"
    
    cursor = connection.execute(sql_command)
    result = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    if result: return dict(zip(column_names, result[0]))
    else: return None