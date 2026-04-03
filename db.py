import pyodbc

def get_db_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=DESKTOP-N2DF03S\\SQLEXPRESS;"
        "DATABASE=SchoolFeeSystemDB;"
        "Trusted_Connection=yes;"
    )
    return conn