import sqlite3

class db_connection:

    def __init__(self):
        self.dbc1 = None
        self.inTransaction = False
        pass

    def create_connection(self):
        self.dbc1 = sqlite3.connect("01Python.db")
        return self.dbc1

    def begin_transaction(self):
        self.query('BEGIN TRANSACTION')

    def query(self, query):
        if (self.dbc1 == None):
            raise Exception("db connection isn't created yet")

        if (query == ''):
            raise Exception("Query cannot be blank")
