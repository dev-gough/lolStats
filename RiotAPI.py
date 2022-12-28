import requests as r
import os
import numpy as np

from dotenv import load_dotenv

class RiotAPI():
    """ riot api wrapper class

        looks for a .env file in the same directory, and looks for a var RIOT_API
    """
    
    def __init__(self) -> None:
        load_dotenv()

        self.api_key = os.getenv("RIOT_API")

    def _handle_req(self,req) -> dict:
        """ handles requests to riots rest api"""
        ending = '?api_key=' + self.api_key
        response = r.get(req + ending)
        code = response.status_code

        if code == 400:
            raise Exception("Bad Request.")
        elif code == 401:
            raise Exception("Unauthorized.")
        elif code == 403:
            raise Exception("New API Key Needed.")
        elif code == 429:
            raise Exception("Rate Limited.")
        elif code != 200:
            print(f"something else: {code}")
        
        return response

    def get_summoner_by_name(self, name: str) -> dict:
        """ gets summoner data

            api calls: 1

            returns:
                {
                    accountId: string,
                    profileIconId: int,
                    revisionData: long,
                    name: string,
                    id: string,
                    puuid: string,
                    summonerLevel: long
                }
            
            accountID: encrypted ID, Max length 56 char
            puuid: encrypted global user id, exact length 78 char
        """
        return self._handle_req('https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + name).json()

    def get_puuid_by_summoner_name(self, name: str) -> str:
        """ returns encrypted puuid
        
            api calls: 1
        """ 
        return self.get_summoner_by_name(name)['puuid']


    def get_challenge_data_by_summoner_name(self, name: str) -> dict:
        """ gets all challenge data
        
            api calls: 2

            returns:
                {
                    totalPoints: {
                        level: string,
                        current: int,
                        max: int,
                        percentile: float
                    },
                    categoryPoints: {
                        "VETERANCY" : {
                            level: string,
                            current: int,
                            max: int,
                            percentile: float
                        },
                    },
                    challenges: [
                        {
                            challengeId: int,
                            percentile: float,
                            level: string,
                            value: int,
                            achievedTime: long
                        },
                    ],
                    preferences: {
                        bannerAccent: string,
                        title: string,
                        challengeIds :[
                            int,
                            int,
                            int
                        ]
                    }
                }
        
        above, where you see a comma where there typically shouldn't be one, assume that there are more elements in the dictionary, and that they follow the same structure.
        this is a big file to work with.  there are 4 major elements of the dict returned, and I care about 2 of them.

        'totalPoints' is used in get_challenge_total_points only, most of the work is done with 'challenges'

        """
        puuid = self.get_puuid_by_summoner_name(name)
        return self._handle_req('https://na1.api.riotgames.com/lol/challenges/v1/player-data/' + puuid).json()

    def get_challenge_data_for_sql(self, name: str) -> list[tuple]:
        """ organizes data into a list of tuples"""
        challenges = self.get_challenge_data_by_summoner_name(name)['challenges']
        data = []

        for challenge in challenges:
            try:
                a_t = challenge['achievedTime']
            except KeyError:
                a_t = None

            c_id = challenge['challengeId']
            p = challenge['percentile']
            l = challenge['level']
            v = challenge['value']

            data.append((c_id,p,l,v,a_t))

        return data

    def get_challenge_total_points(self, name: str) -> int:
        """ returns total challenge points for a summoner name"""
        points = self.get_challenge_data_by_summoner_name(name)['totalPoints']
        return points['current']