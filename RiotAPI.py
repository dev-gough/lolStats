import requests as r
import os

from dotenv import load_dotenv

load_dotenv()

RIOT_API = os.getenv("RIOT_API")
ending = '?api_key=' + RIOT_API

class RiotAPI() :
    
    def __init__(self, api_key=RIOT_API) -> None :
        self.api_key = api_key

    # Summoner methods

    def get_summoner_by_name(self, name: str) -> dict :
        return r.get('https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + name + ending).json()

    def get_puuid_by_summoner_name(self, name: str) -> str : 
        return self.get_summoner_by_name(name)['puuid']


    def get_challenge_data_by_summoner_name(self, name: str) -> dict :
        puuid = self.get_puuid_by_summoner_name('name')
        return r.get('https://na1.api.riotgames.com/lol/challenges/v1/player-data/' + puuid + ending).json()

    def get_challenge_data_for_sql(self, name: str) -> list[tuple] :
        challenges = self.get_challenge_data_by_summoner_name(name)['challenges']
        data = []

        for challenge in challenges:
            try:
                a_t = challenge['achievedTime']
            except KeyError :
                a_t = None

            c_id = challenge['challengeId']
            p = challenge['percentile']
            l = challenge['level']
            v = challenge['value']

            data.append((c_id,p,l,v,a_t))

        return data
    
    def get_challenge_total_points(self, name: str) -> int :
        data = self.get_challenge_data_by_summoner_name(name)
        return data['totalPoints']['current']
