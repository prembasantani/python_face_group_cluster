import sqlite3

class db_connection:

    def __init__(self):
        self.dbc1 = None
        self.inTransaction = False
        self.db_cursor
        pass

    def create_connection(self):
        self.dbc1 = sqlite3.connect("01Python.db", isolation_level=None)
        self.db_cursor = self.dbc1.cursor()

        self.check_if_table_exists()

        return self.dbc1

    def check_if_table_exists(self):
        if (self.dbc1 == None):
            raise Exception("db connection isn't created yet")

        data = self.query("SHOW TABLES LIKE 'image_hashes'")
        if (len(data) == 0):
            self.query("SHOW TABLES LIKE 'image_hashes'")


    def begin_transaction(self):
        self.query('BEGIN TRANSACTION')

    def query(self, query):
        if (self.dbc1 == None):
            raise Exception("db connection isn't created yet")

        if (query == ''):
            raise Exception("Query cannot be blank")

        execution = self.db_cursor.execute(query)
        print(f"execution : execution{execution}")
        return self.db_cursor.fetchall()
