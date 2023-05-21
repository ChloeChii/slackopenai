import os
import sqlite3


def retriveMsg():
    db_name = os.environ['DB_NAME']
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Retrieve the 10 most recent messages from the database
    c.execute("SELECT * FROM messages ORDER BY ts DESC LIMIT 10")
    # c.execute("SELECT * FROM messages LIMIT 10")os.environ['CHANNEL_ID']
    messages = c.fetchall()
    message_count = len(messages)
    # print("message_count======")
    # print(message_count)
    for message in messages:
        # print(message)
        ts = message[0]
        role = message[1]
        content = message[2]
        print(content)
        # print(ts)

    conn.close()