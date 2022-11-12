# database initialization
import sqlite3

database = sqlite3.connect('data.db')
cur = database.cursor()


# returning record from database
def record(size) -> int or float:
    r = cur.execute(f"""
            SELECT record FROM records
            WHERE size={size}
            """).fetchone()

    return 0 if r is None else float(r[0])
