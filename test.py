import pyodbc

CONNECTION_STRING = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:notepadai-dbserver.database.windows.net,1433;Database=notepadai-db;Uid=notepad-administrator;Pwd=Cloud2024;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

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
    
def insert_notebook(title, userID, userEMAIL):
    connection = pyodbc.connect(CONNECTION_STRING)
    stored_name = f"{title}-{userEMAIL}"
    sql_command = f"INSERT INTO [dbo].[Notebooks] (StoredNotebookName, NotebookTitle, UserID) VALUES ('{stored_name}', '{title}', {userID})"
    connection.execute(sql_command)
    connection.commit()
    connection.close()
    
def find_user_notebooks(userID):
    connection = pyodbc.connect(CONNECTION_STRING)
    sql_command = f"SELECT * FROM [dbo].[Notebooks] WHERE UserID = '{userID}'"
    cursor = connection.execute(sql_command)
    
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return results
    
    
if __name__ == "__main__":
    #insert_user("Mario", "Rossi", "m.rossi@unisa.it", "mrossi1")
    
    #insert_notebook("Notebook1", 2, "m.rossi@unisa.it")
    #insert_notebook("Notebook1", 2, "m.rossi@unisa.it")
    #insert_notebook("Notebook1", 2, "m.rossi@unisa.it")
    #insert_notebook("Notebook1", 2, "m.rossi@unisa.it")
    #insert_notebook("Notebook1", 2, "m.rossi@unisa.it")
    delete_user("m.rossi@unisa.it")