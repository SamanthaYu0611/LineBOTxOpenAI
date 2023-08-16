import requests
import os
import json
def chat(msg):
    apiUrl = "https://api.openai.com/v1/completions"
    data1 = {
            "model": "text-davinci-003",
            "prompt": msg,
            "max_tokens":200,
            "temperature":0.8,
            "n":1
            }
    key = os.getenv("OPENAI_API_KEY")
    key2 = f'Bearer {key}'
    headers = {"Content-Type":"application/json", "Authorization": key2}
    response = requests.post( apiUrl, json = data1, headers = headers)
    b = response.json()
    print(b)
    return b["choices"][0]["text"].replace("\n","")
