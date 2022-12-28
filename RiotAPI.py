import requests as r
import os
import numpy as np

from dotenv import load_dotenv

class RiotAPI():
    
    def __init__(self) -> None:
        load_dotenv()

        self.api_key = os.getenv("RIOT_API")

    def _handle_req(self,req) -> dict:
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

    # Summoner methods

    def get_summoner_by_name(self, name: str) -> dict:
        return self._handle_req('https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + name).json()

    def get_puuid_by_summoner_name(self, name: str) -> str: 
        return self.get_summoner_by_name(name)['puuid']


    def get_challenge_data_by_summoner_name(self, name: str) -> dict:
        puuid = self.get_puuid_by_summoner_name(name)
        return self._handle_req('https://na1.api.riotgames.com/lol/challenges/v1/player-data/' + puuid).json()

    def get_challenge_data_for_sql(self, name: str) -> list[tuple]:
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
        challenges = self.get_challenge_data_by_summoner_name(name)['challenges']
        points = np.sum([x['value'] for x in challenges])
        return points