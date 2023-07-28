from PIL import Image
import openai
import os
from io import BytesIO
import requests

openai.api_key = os.getenv("OPENAI_API_KEY")

def chat(prompt):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        temperature=0.7,
        max_tokens=3000
    )

    reply_text = ""
    for choice in response.choices:
        reply_text += choice.text
        
    return reply_text.replace('\n', '')

def image(msg):
    response = openai.Image.create(
        prompt=msg,
        size="256x256",
        n=1
    )
    imageUrl = response['data'][0]['url']
    
    return imageUrl