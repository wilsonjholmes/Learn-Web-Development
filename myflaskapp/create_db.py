import sqlite3
sqlite_file = 'myflaskapp.db'
conn = sqlite3.connect(sqlite_file)
conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(100), email VARCHAR(100), username VARCHAR(30), password VARCHAR(100), register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
conn.execute("CREATE TABLE articles (id INTEGER PRIMARY KEY AUTOINCREMENT, title VARCHAR(255), author VARCHAR(100), body TEXT, create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
conn.commit()