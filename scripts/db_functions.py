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
    
def insert_notebook(title, userID, userEMAIL, type):
    connection = pyodbc.connect(CONNECTION_STRING)
    stored_name = f"{title}-{userEMAIL}"
    sql_command = f"INSERT INTO [dbo].[Notebooks] (StoredNotebookName, NotebookTitle, NotebookType, UserID) VALUES ('{stored_name}', '{title}', '{type}', {userID})"
    connection.execute(sql_command)
    connection.commit()
    connection.close()
    
def delete_notebook(id):
    connection = pyodbc.connect(CONNECTION_STRING)
    sql_command = f"DELETE FROM [dbo].[Notebooks] WHERE NotebookID = {id}"
    connection.execute(sql_command)
    connection.commit()
    connection.close()
    
def get_notebook_by_id(id):
    connection = pyodbc.connect(CONNECTION_STRING)
    sql_command = f"SELECT * FROM [dbo].[Notebooks] WHERE NotebookID = {id}"
    cursor = connection.execute(sql_command)
    
    column_names = [column[0] for column in cursor.description]
    result = cursor.fetchall()
    if result: return dict(zip(column_names, result[0]))
    else: return None

def get_notebook_by_title(title):
    connection = pyodbc.connect(CONNECTION_STRING)
    sql_command = f"SELECT * FROM [dbo].[Notebooks] WHERE NotebookTitle = {title}"
    cursor = connection.execute(sql_command)
    
    column_names = [column[0] for column in cursor.description]
    result = cursor.fetchall()
    if result: return dict(zip(column_names, result[0]))
    else: return None
    
def find_user_notebooks(userID):
    connection = pyodbc.connect(CONNECTION_STRING)
    sql_command = f"SELECT * FROM [dbo].[Notebooks] WHERE UserID = '{userID}'"
    cursor = connection.execute(sql_command)
    
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return results