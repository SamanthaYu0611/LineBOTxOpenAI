from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot import LineBotApi
from linebot.models import ImageMessage, ImageSendMessage
from linebot.models import TextSendMessage   # 載入 TextSendMessage 模組
import json
from ai import chat,image
import os
import datetime

app = Flask(__name__)

CHANNEL_SECRET = os.getenv("LINEBOT_CHANNEL_SECRET")
CHANNEL_ACCESS_TOKEN = os.getenv("LINEBOT_ACCESS_TOKEN")

@app.route("/", methods=['GET'])
def home():
    return "Hi"

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    print(json_data)

    try:
        line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
        handler = WebhookHandler(CHANNEL_SECRET)
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']         # 取得 reply token
        msg = json_data['events'][0]['message']['text']   # 取得使用者發送的訊息
        # text_message = TextSendMessage(text = image(msg))#TextSendMessage(text=msg)          # 設定回傳同樣的訊息
        # line_bot_api.reply_message(tk,text_message)       # 回傳訊息
        
        image_url = image(msg)
        image_message = ImageSendMessage(
            original_content_url=image_url,
            preview_image_url=image_url
        )
        
        line_bot_api.reply_message(tk, image_message)     # 回傳圖片
        
        # 傳送者資訊
        userID = json_data['events'][0]['source']['userId']
        userProfile = line_bot_api.get_profile(userID)
        userName = userProfile.display_name       #Line名稱
        userPicture = userProfile.picture_url     #Line頭貼

        # 時間戳記
        Time = json_data['events'][0]['timestamp']
        utcTime = datetime.datetime.utcfromtimestamp(Time / 1000.0)
        timeFormat = "%Y-%m-%d %H:%M:%S"
        localTime = utcTime + datetime.timedelta(hours=8)
        sendTime = localTime.strftime(timeFormat)

        userRequest = {"Time":sendTime,"UserInput":msg,"UserName":userName,"UserPicture":userPicture}
        print(userRequest)
        
        with open("text.json","a",encoding="utf-8") as fp:
            json.dump(userRequest,fp,ensure_ascii=False,indent=4)
            fp.write("\n")
    
    except Exception as e:
        print('error: ' + str(e))
    return 'OK'

app.run(port="5000")


