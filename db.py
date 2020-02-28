import sqlite3


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS api (id INTEGER PRIMARY KEY, url text, token text, frq integer, direct text, auto_run boolean)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM api")
        rows = self.cur.fetchall()
        return rows

    def last(self):
        self.cur.execute("SELECT * FROM api ORDER BY id DESC LIMIT 1")
        return self.cur.fetchone()

    def insert(self, url, token, frq, direct, auto_run):
        self.cur.execute("INSERT INTO api VALUES (NULL, ?, ?, ?, ?, ?)", (url, token, frq, direct, auto_run))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM api WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, url, token, frq, direct, auto_run):
        self.cur.execute("UPDATE api SET url = ?, token = ?, frq = ?, direct = ?, auto_run = ? WHERE id = ?", (url, token, frq, direct, auto_run, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
