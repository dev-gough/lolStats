from RiotAPI import RiotAPI
from SQLiteHandler import SQLiteHandler

def new_db(database_file: str):
    s = SQLiteHandler(database_file)
    j = r.get_challenge_data_for_sql('devy10')
    s.insert(j)
    

if __name__ == '__main__':
    db = 'challenges.db'
    s = SQLiteHandler(db)
    r = RiotAPI()

    