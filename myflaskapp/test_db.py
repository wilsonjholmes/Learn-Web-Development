import sqlite3

name = "Wilson Holmes"
email = "wilson@gmail.com"
username = "wilson"
password = "12345"

sqlite_file = 'myflaskapp.db'
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()
cur.execute("INSERT INTO users(name, email, username, password) VALUES(?, ?, ?, ?)", (name, email, username, password))
conn.commit()
conn.close()