import sqlite3

class SQLiteHandler():
    
    def __init__(self, database_file: str) -> None:
        self.database_file = database_file
        self.con = sqlite3.connect(database_file)
        self.cur = self.con.cursor()

        self.cur.execute("CREATE TABLE IF NOT EXISTS challenge(id, percentile, level, value, achievedTime)")
    
    def _insert_many(self, data: list[tuple]):
        self.cur.executemany("INSERT INTO challenge VALUES(?,?,?,?,?)", data)
        self.con.commit()

    def insert(self, data: tuple):
        if type(data) == list :
            try:
                self._insert_many(data)
                return
            except sqlite3.ProgrammingError:
                raise TypeError("Provided data unusable.")

        self.cur.execute("INSERT INTO challenge VALUES(?,?,?,?,?)", data)
        self.con.commit()
    
    def update(self, data: tuple):
        """ updates a challege value

            parameters:
                data (tuple): of form (percentile, level, value, achievedTime, id)
        
        """
        sql = """UPDATE challenge
        SET percentile = ?,
            level = ?,
            value = ?,
            achievedTime = ?
        WHERE id = ?"""

        self.cur.execute(sql,data)
        self.con.commit()

    
    def get_data(self) -> dict:
        res = self.cur.execute("SELECT * FROM challenge")
        return res.fetchall()