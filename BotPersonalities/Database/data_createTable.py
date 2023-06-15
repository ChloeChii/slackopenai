import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()
db_name = os.environ['DB_NAME']
conn = sqlite3.connect(db_name)
c = conn.cursor()

c.execute('''CREATE TABLE messages
        (ts timestamp primary key, role text, content text)'''
)

conn.commit()
conn.close()
# def create_DB():
    
