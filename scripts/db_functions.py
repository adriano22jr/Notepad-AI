import pyodbc, app_config

SERVER = app_config.DB_NAME
DATABASE = "notepadai-db"
DRIVER = "{ODBC Driver 18 for SQL Server}"
CONNECTION_STRING = f"Driver={DRIVER};Server=tcp:{SERVER},1433;Database={DATABASE};Uid={app_config.DB_USERNAME};Pwd={app_config.DB_PASSWORD};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

def insert_user(firstname, lastname, email, username):
    connection = pyodbc.connect(CONNECTION_STRING)
    sql_command = f"INSERT INTO [dbo].[Users] (Email, FirstName, LastName, Username) VALUES ({email}, {firstname}, {lastname}, {username});"
    connection.execute(sql_command)
    connection.close()
    
def check_exising_user(email):
    connection = pyodbc.connect(CONNECTION_STRING)
    sql_command = f"SELECT * FROM [dbo].[Users] WHERE Email = '{email}'"
    
    cursor = connection.execute(sql_command)
    result = cursor.fetchall()
    if len(result) == 1:
        return result[0]
    else:
        return None