import sqlite3

class Database:
    def __init__(self, dbfile):
        self.db = sqlite3.connect(dbfile, isolation_level=None)
        self.cur = self.db.cursor

    def initial(self, table, attributes):
        self.cur.execute("CREATE TABLE IF NOT EXISTS " + table + " (" + attributes + ")")

    def get():
        pass

    def set():
        pass