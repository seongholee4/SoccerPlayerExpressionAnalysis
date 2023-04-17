import re
import json
import os
import requests

from dotenv import load_dotenv

def get_access_id(nickname, api_key):
    url = f"https://api.nexon.co.kr/fifaonline4/v1.0/users?nickname={nickname}"
    headers = {'Authorization': api_key}

    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        raise RuntimeError(f"Request status code : {res.status_code}. Try again!")
    res = res.json()
    return res["accessId"]

def get_spid():
    url = f"https://static.api.nexon.co.kr/fifaonline4/latest/spid.json"
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f"Request status code : {res.status_code}. Try again!")
    res = res.json()
    return res

def get_spid():
    url = f"https://static.api.nexon.co.kr/fifaonline4/latest/spid.json"
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f"Request status code : {res.status_code}. Try again!")
    res = res.json()
    return res

def get_spposition():
    url = f"https://static.api.nexon.co.kr/fifaonline4/latest/spposition.json"
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f"Request status code : {res.status_code}. Try again!")
    res = res.json()
    return res

def create_spposition():
    # get po_length from supposition.json
    with open('spposition.json', 'r') as f:
        json_data = json.load(f)
        po_length = len(json_data)
    po_list = [] # Initialize an empty list to store 'supposition' values
    for item in json_data:
        po = item['spposition']
        po_list.append(po)
    return po_length, po_list

def create_id():
    with open('spid.json', 'r') as f:
        json_data = json.load(f)
        id_length = len(json_data)
    id_list = []  # Initialize an empty list to store 'id' values
    for item in json_data:
        id = item['id']
        id_list.append(id)

    return id_length, id_list

def save_players_as_json_object():
    json_array = []
    for i in id_list:
        for p in po_list:
            player = {"id": i, "po": p}
            json_array.append(player)
    json_string = json.dumps(json_array, indent=4)
    # store json_string to a file
    with open('players.json', 'w') as file:
        file.write(json_string)


if __name__ == "__main__":
    load_dotenv()

    api_key = os.environ.get('API_KEY')
    if api_key is None:
        raise RuntimeError("API_KEY is not set")
    
    # get access id
    access_id = get_access_id("마음이부자", api_key)
    # print("Access ID: ", access_id)

    # get spid
    spid = get_spid()
    # store spid as a json file
    with open('spid.json', 'w') as file:
        json.dump(spid, file)
    
    # get spposition
    spposition = get_spposition()
    # store spposition as a json file
    with open('spposition.json', 'w') as file:
        json.dump(spposition, file)


    id_length, id_list = create_id()
    po_length, po_list = create_spposition()
    print(id_length)
    print(po_length)
    '''
    Lacks of memory to iterate all players (61181) with all different positions (29)
    The API needs to be called 61181 * 29 times
    Rather, It would be useful if the API provider (NEXON DEVELOPERS) provides a way to get all players' information in the following way.
    players = [
        {"id": 1, "name": "Player1", "positions": ["position1", "position2"]},
        {"id": 2, "name": "Player2", "positions": ["position1", "position3"]},
        # ...
    ]
    So that, I can iterate all players with the corresponding positions for a single API call.
    '''

    '''
    Furthermore, I was trying to use "TOP 10,000 랭커 유저가 사용한 선수의 20경기 평균 스탯" API
    https://developers.nexon.com/fifaonline4/api/11/22
    But, I couldn't find any API to get the information.
    "한번에 너무 많은 선수목록을 입력할 경우 413 Request Entity Too Large 에러가 반환될 수 있습니다.
    한번에 호출하는 선수의 수는 50명이 적당합니다."
    '''
    # save players as json object
    # save_players_as_json_object()

    # with open('players.json', 'r') as file:
    #     json_data = json.load(file)
    
    # print(json_data)
    # url = f"https://api.nexon.co.kr/fifaonline4/v1.0/rankers/status?matchtype={matchtype}&players={players}"
    # headers = {
    #     "Authorization": api_key
    # }
    # res = requests.get(url, headers=headers)
            # if res.status_code != 200:
            #     raise RuntimeError(f"Request status code : {res.status_code}. Try again!")
    # res = res.json()
    # print(res)

