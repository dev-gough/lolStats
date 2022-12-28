import time
import requests
from RiotAPI import RiotAPI
from SQLiteHandler import SQLiteHandler

NAME = 'devy10'

def shift_tuple(t: tuple):
    """ shifts a tuple left one, with index 0 wrapping to -1 """
    temp = list(t)
    temp[:] = temp[1:] + [temp[0]]
    return temp

def setup_db():
    """" completes the initial setup of the database """
    j = r.get_challenge_data_for_sql(NAME)
    s.insert(j)

def print_values(old, new, i, verbose=False):

    config = r.challenge_config
    challenge = [x for x in config if x['id'] == old[i][0]][0]
    
    print(challenge['localizedNames']['en_US']['name'])
    print(challenge['localizedNames']['en_US']['shortDescription'])

    if verbose:
        print(f"Challenge ID: {old[i][0]}")
        print(f"Old value: {old[i][3]}")
        print(f"New value: {new[i][3]}")

    print(f"Difference: +{new[i][3] - old[i][3]}")
    print('--------------------------------')

def handle_update():
    """ updates database file with new values

        both old and new are of form [(id,percentile,level,value,achievedTime),(),...]
    
        old data gets read from the database, and the new data comes from the RiotAPI

        the function then just loops through, comparing each value (index 3)

        when the values differ, the table gets updated with the new value, which needs to be shifted
        to the left one index, such that id is at the last index (percentile,level,value,achievedTime,id)
    """
    old = s.get_data()
    new = r.get_challenge_data_for_sql(NAME)

    if len(old) != len(new):
        print("new challenge added?")
    
    # iterate through each element to update
    for i in range(len(old)):
        if old[i][0] != new[i][0]:
            raise Exception("Not comparing the same ID.")

        if old[i][3] != new[i][3]:
            print_values(old,new,i)
            data = shift_tuple(new[i])
            s.update(data)
    
    return r.get_challenge_total_points(NAME)
    
def checker_loop(iters=None, interval=60):
    """ main function loop 

        checks every `interval` seconds if there needs to be an update

        if the total points differ, then a challenge must've progressed, so run update
    """
    i = 0
    total_points = r.get_challenge_total_points(NAME)
    while True:
        if iters and i >= iters:
            break

        print(f"Iteration: {i}")
        check = r.get_challenge_total_points(NAME)
        print(f"Old: {total_points}\nNew: {check}\n")
        if total_points != check:
            total_points = handle_update()

        time.sleep(interval)
        i += 1
    
        
if __name__ == '__main__':
    db = 'challenges.db'
    s = SQLiteHandler(db)
    r = RiotAPI()

    setup_db()
    checker_loop()
