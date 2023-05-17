import sqlite3
from flask import g

def connect_to_DB():
    sql = sqlite3.connect("C:/Users/USER/Desktop/ALX/quizApp/app_database.db")
    sql.row_factory = sqlite3.Row
    return sql
    
    
def getDatabase():
    if not hasattr(g, "app_database_db"):
        g.app_database_db = connect_to_DB()
    return g.app_database_db