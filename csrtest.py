import sys
import requests
import os
from dotenv import load_dotenv
import json

# .env 파일 로드
load_dotenv()

client_id = os.getenv("CSR_ID")
client_secret = os.getenv("CSR_SECRET")
audio = os.getenv("AUDIO_FILE")

lang = "Kor" # 언어 코드 ( Kor, Jpn, Eng, Chn )
url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + lang
data = open('ttt.mp3', 'rb')
headers = {
    "X-NCP-APIGW-API-KEY-ID": client_id,
    "X-NCP-APIGW-API-KEY": client_secret,
    "Content-Type": "application/octet-stream"
}
response = requests.post(url,  data=data, headers=headers)
rescode = response.status_code
if(rescode == 200):
    # data = json.loads(response.text)
    data = response.text[9:-2]
    # print (response.text[9:-2])
    url = "http://127.0.0.1:5000/api/text"
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url,  data=data, headers=headers)
    rescode = response.status_code
    if(rescode == 200):
        print (response.text)
    else:
        print("Error : " + response.text)
else:
    print("Error : " + response.text)