import sqlite3

conn = sqlite3.connect("data/memory.db")
c = conn.cursor()


class MemoryUnit:
    """
                                        METADATA OF CLASS
    ---------------------------------------------------------------------------------------
    Connection pool: sqlite3 :: conn = sqlite3.connect("data/memory.db")
    ---------------------------------------------------------------------------------------
    Cursor of Database: sqlite3 :: c = conn.cursor()
    ---------------------------------------------------------------------------------------
    Total methods in class : MemoryUnit :: 3 methods, 1 initialisation method
    ---------------------------------------------------------------------------------------
    Server overdrive : Memory end :: conn.commit() ::: c.close() ::: conn.close()
    ---------------------------------------------------------------------------------------

    =======================================================================================
    # Method: create_table(self, true): if there is no table already created, create one, else pass.
    # using SQL for creating table-- CREATE TABLE IF NOT EXISTS memoryUnit(question TEXT, answer TEXT)
    # and creating 2 coloumns for question and answer whose data type is string
    #
    # Method: data_entry(self, question, answer): takes the question and answer, so that we can
    # assign question along with answer in the same row. SQL used.
    # INSERT INTO memoryUnit (question, answer) VALUES (?, ?)", (self.question, self.answer)
    =======================================================================================

    """
    def __init__(self):
        self.true = None
        self.question = None
        self.answer = None
        self.searchable = None
        self.create_table(True)

    def create_table(self, true):
        self.true = true
        if self.true:
            c.execute("CREATE TABLE IF NOT EXISTS memoryUnit(question TEXT, answer TEXT)")
            conn.commit()
        else:
            pass

    def data_entry(self, question, answer):
        self.question = question
        self.answer = answer
        c.execute("INSERT INTO memoryUnit (question, answer) VALUES (?, ?)", (self.question, self.answer))
        conn.commit()

    def read_from_db(self, searchable):
        self.searchable = searchable
        c.execute("SELECT * FROM memoryUnit")
        for row in c.fetchall():
            if self.searchable in row[0]:
                return row[1]
            else:
                mem_in = input("I don't know ")
                self.data_entry(self.searchable, mem_in)
                return None

    def read_all(self):
        c.execute("SELECT * FROM memoryUnit")
        for row in c.fetchall():
            print(row)

# MemoryUnit().read_all()