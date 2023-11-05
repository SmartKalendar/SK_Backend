from flask import Flask
from flask import request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

API_KEY= os.getenv("API_KEY")

url = "https://api.openai.com/v1/chat/completions"
data = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.8,
    "max_tokens": 2048,
    "messages": [
        {"role": "system", "content": "너는 문장을 아래 json 형태로 요약해야한다. 또한 필요한 정보가 없는 경우 -으로 채운다."},
        {"role": "system", "content": "summary, location, description, start, end에 대한 정보를 입력해야한다.\n start와 end는 dateTime과 timeZone으로 구성되어있다.\n timeZone은 Asia/Seoul로 고정한다.\n dateTime은 YYYY-MM-DDTHH:MM:SS+09:00 형태로 입력한다.\n - 요약한 json 형태만 반환한다."},
        {"role": "user", "content": ReadCsrResult}, 
    ]
    }
headers: {
    "Authorization": "Bearer " + API_KEY,
    "Content-Type": 'application/json',
  },
response = requests.post(url,  data=data, headers=headers)
rescode = response.status_code
if(rescode == 200):
    print (response.text)
else:
    print("Error : " + response.text)

@app.route("/api/text", methods=["POST"])
def TextMassageMaker(API_KEY=API_KEY):    
    input = request.get_json()
    
    # request body 값 
    text = input["text"]

    # set api key
    openai.api_key = API_KEY
    
    # Call the chat GPT API
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
              {"role": "system", "content": "너는 문장을 아래 json 형태로 요약해야한다. 또한 필요한 정보가 없는 경우 -으로 채운다."},
              {"role": "system", "content": "summary, location, description, start, end에 대한 정보를 입력해야한다.\n start와 end는 dateTime과 timeZone으로 구성되어있다.\n timeZone은 Asia/Seoul로 고정한다.\n dateTime은 YYYY-MM-DDTHH:MM:SS+09:00 형태로 입력한다.\n - 요약한 json 형태만 반환한다."},
              {"role": "user", "content": f"${text}"},
        ],
        temperature=0.8,
        max_tokens=2048
    )

    message_result = completion["choices"][0]["message"]["content"].encode("utf-8").decode()

    return jsonify({"result": message_result})

if __name__ == '__main__':
    app.run(host = '127.0.0.1', debug=True, port=5000)