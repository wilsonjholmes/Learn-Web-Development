import sqlite3
import time

sqlite_file = 'db.sqlite'

try:
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    timestamp = timestamp_begin
    while timestamp <= timestamp_end:
        print("Iterations left :", (timestamp_end-timestamp)/pitch)
        measure = randint(0, 9)
        conn.execute("INSERT INTO measures (timestamp, measure) VALUES ({timestamp}, {measure})".format(timestamp=timestamp, measure=measure))
        conn.commit()
        timestamp += pitch
except Exception as e:
    conn.rollback()
    raise e
finally:
    conn.close()