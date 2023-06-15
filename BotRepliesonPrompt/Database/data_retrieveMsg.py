import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()

def retriveMsg():
    
    db_name = os.environ['DB_NAME']
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Retrieve the 10 most recent messages from the database
    c.execute("SELECT * FROM messages ORDER BY ts DESC LIMIT 10")
    messages = c.fetchall()
    message_count = len(messages)
    for message in messages:
        ts = message[0]
        role = message[1]
        content = message[2]

    conn.close()