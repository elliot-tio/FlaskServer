from flask import Flask, request, jsonify
import requests, json
import os

# Init app
app = Flask(__name__)
API_KEY = 'RGAPI-8ce66809-4d59-4e9e-ab5f-af36f2bc4401'

# Que constants
RANKED_FLEX = 440
RANKED_SOLO = 420
NORMAL_DRAFT = 400
NORMAL_BLIND = 430 

# User Info
def getUserInfo(region, name):
    url = 'https://%s.api.riotgames.com/lol/summoner/v4/summoners/by-name/%s?api_key=%s'%(region, name, API_KEY)
    response = requests.get(url).json()
    # user_id = response["id"]
    # account_id = reponse["accountId"]
    # summoner_level = response["summonerLevel"]
    # puuid = response["puuid"]
    return response

def getMatchesInfo(region, accountId):
    url = 'https://%s.api.riotgames.com/lol/match/v4/matchlists/by-account/%s?api_key=%s'%(region, accountId, API_KEY)
    response = requests.get(url).json()
    matches = [i for i in response["matches"] if (i["role"] == 'DUO' or i["role"] == 'DUO_SUPPORT') and (i["queue"] == RANKED_FLEX or i["queue"] == RANKED_SOLO)]
    return matches

@app.route('/', methods=['GET'])
def results():
    region = 'na1'
    results = getUserInfo(region, 'bo9')
    accountId = results["accountId"]
    matches = getMatchesInfo(region, accountId)
    return 'You have played ' + str(len(matches)) + 'games with premades.'


# Run Server
if __name__ == '__main__':
    app.run(debug=True)