import sys
import requests
import json
from urllib.request import urlopen
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

client_id = os.getenv("CSR_ID")
client_secret = os.getenv("CSR_SECRET")
audio = os.getenv("AUDIO_FILE")

headers = {
    "X-NCP-APIGW-API-KEY-ID": client_id,
    "X-NCP-APIGW-API-KEY": client_secret,
    "Content-Type": "application/octet-stream"
}

language = "Kor" # 언어 코드 ( Kor, Jpn, Eng, Chn )
csr_rest_api_url= "https://naveropenapi.apigw.ntruss.com/recog/v1/stt" 
content_url = audio # 음성 파일 url

url = csr_rest_api_url +"?lang=" +language
data = urlopen(content_url)

response = requests.post(url, data=data, headers=headers)
rescode = response.status_code
if(rescode == 200):
    print (response.text)
else:
    print("Error : " + response.text)
