import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()

def checkDB():
    # Create a connection to the database with the check_same_thread parameter set to False
    db_name = os.environ['DB_NAME']
    conn = sqlite3.connect(db_name, check_same_thread=False)

    # Try to execute a query and catch any exceptions
    try:
        c = conn.cursor()
        c.execute('SELECT * FROM messages limit 1')
        rows = c.fetchall()
        print(rows)
    except sqlite3.Error as e:
        print(f'Error executing query: {e}')

    # Close the connection to the database
    conn.close()