import time
import requests
from RiotAPI import RiotAPI
from SQLiteHandler import SQLiteHandler

NAME = 'devy10'

def shift_tuple(t: tuple):
    temp = list(t)
    temp[:] = temp[1:] + [temp[0]]
    return temp

def setup_db():
    j = r.get_challenge_data_for_sql(NAME)
    s.insert(j)

def handle_update():
    old = s.get_data()
    new = r.get_challenge_data_for_sql(NAME)

    if len(old) != len(new):
        print("new challenge added?")
    
    # iterate thru each element to update
    for i in range(len(old)):
        if old[i][0] != new[i][0]:
            raise Exception("Not comparing the same ID.")

        if old[i][3] != new[i][3]:
            print(f"Challenge ID: {old[i][0]}")
            print(f"Old value: {old[i][3]}")
            print(f"New value: {new[i][3]}")
            print(f"Difference: {new[i][3] - old[i][3]}")

            data = shift_tuple(new[i])
            s.update(data)

    
def checker_loop(iters=None, interval=60):
    i = 0
    total_points = r.get_challenge_total_points(NAME)
    while True:
        if iters and i >= iters:
            break

        print(f"Iteration: {i}")
        check = r.get_challenge_total_points(NAME)
        print(f"Old: {total_points}\nNew: {check}\n")
        if total_points != check:
            handle_update()

        time.sleep(interval)
        i += 1
    
        
if __name__ == '__main__':
    db = 'challenges.db'
    s = SQLiteHandler(db)
    r = RiotAPI()

    setup_db()
    checker_loop()