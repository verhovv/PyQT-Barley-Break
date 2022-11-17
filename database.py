import sqlite3

# database initialization
database = sqlite3.connect('assets/data.db')
cur = database.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS records (
    size INT, record INT
    )
""")


# returning record from database
def record(size) -> int or float:
    r = cur.execute(f"""
            SELECT record FROM records
            WHERE size={size}
            """).fetchone()

    return 0 if r is None else float(r[0])
