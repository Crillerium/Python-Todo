import sqlite3
conn = sqlite3.connect(sys.argv[0].replace('plandb.py','plan.db'))
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS plans (
        id INTEGER PRIMARY KEY,
        plan TEXT NOT NULL,
        duedate DATE NOT NULL
    )
''')
conn.commit()