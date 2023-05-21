import os
import sqlite3

from dotenv import load_dotenv
from slack import WebClient
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError

# load the .env file
load_dotenv()
def updateSchema():
    # Connect to the database
    db_name = os.environ['DB_NAME']
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Modify the SQL statement to add "ts" column with timestamp data type
    sql = '''ALTER TABLE messages
            ADD COLUMN ts timestamp'''

    # Execute the modified SQL statement
    c.execute(sql)

    # Commit the changes to the database
    conn.commit()

    # Close the connection
    conn.close()
    #This code snippet assumes you are using SQLite as your database engine. If you are using a different database engine, the syntax for adding a column with a timestamp data type may be slightly different.





