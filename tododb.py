import sqlite3
import sys
conn = sqlite3.connect(sys.argv[0].replace('tododb.py','todo.db'))
c = conn.cursor()
c.execute("CREATE TABLE todos (id INTEGER PRIMARY KEY, task TEXT)")
conn.commit()
conn.close()