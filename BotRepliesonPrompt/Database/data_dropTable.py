import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()

# Connect to the database
def dropTable():
    db_name = os.environ['DB_NAME']
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Drop the "messages" table
    c.execute('DROP TABLE IF EXISTS messages')

    # Commit the changes to the database
    conn.commit()

    # Close the connection
    conn.close()