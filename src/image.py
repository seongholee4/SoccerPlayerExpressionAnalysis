
'''
 특정 선수들은 이미지가 존재하지 않을 수 있습니다.
    이미지가 존재하지 않는 선수들은 제외하고 이미지를 다운로드합니다.
    https://static.api.nexon.co.kr/fifaonline4/latest/spid.json


Load all the images from the FIFA API and save them to the images folder

Semantic Segmentation

'''
import re
import json
import os
import requests

from dotenv import load_dotenv

def get_spid():
    url = f"https://static.api.nexon.co.kr/fifaonline4/latest/spid.json"
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f"Request status code : {res.status_code}. Try again!")
    res = res.json()
    return res

# GET선수 고유 식별자(spid)로 선수 액션샷 이미지 조회
def get_playersAction_image(spid, api_key):
    url = f"https://fo4.dn.nexoncdn.co.kr/live/externalAssets/common/playersAction/p{spid}.png"
    headers = { "Authorization": api_key }
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"Request status code : {res.status_code}. Try again!")
        # raise Exception("Failed to fetch playersAction_image. ")
    return res.content, res.status_code

# GET선수 고유 식별자(spid)로 선수 이미지 조회
def get_players_image(spid, api_key):
    url = f"https://fo4.dn.nexoncdn.co.kr/live/externalAssets/common/players/p{spid}.png"
    headers = { "Authorization": api_key }
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"Request status code : {res.status_code}. Try again!")
        # raise Exception("Failed to fetch players_image.")
    return res.content, res.status_code

if __name__ == "__main__":
    load_dotenv()

    api_key = os.environ.get('API_KEY')
    if api_key is None:
        raise RuntimeError("API_KEY is not set")
    
    # get spid
    spid = get_spid()
    # store spid as a json file
    with open('spid.json', 'w') as file:
        json.dump(spid, file)

    # for each spid, get the image
    for item in spid:
        id = item['id']
        name = item['name']
        try:
            image, status_code = get_playersAction_image(id, api_key)
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch player image after multiple retries: {e}")
            continue

        filename = f"images/{name}_{id}.png"
        if status_code == 200:
            if not os.path.exists(filename):  # Check if the file already exists
                with open(f"images/{name}_{id}.png", "wb") as file:
                    file.write(image)
                    print(f"Image saved for {name} with ID {id}")
                # print(f"Image file for {name} with ID {id} already exists")
        # else:
            # print(f"Failed to download image for {name} with ID {id} and status code {status_code}")
        