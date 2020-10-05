from flask import Flask,request,abort
import os

from linebot import (
    LineBotApi,WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent,TextMessage,TextSendMessage
)

import requests
import json
import datetime



app = Flask(__name__)



CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route('/')
def hello():
    return "HELLO"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=callholo(event.message.text)))



def callholo(text):
    date = datetime.datetime.today().strftime("%Y/%m/%d")
    res = requests.get(url='http://api.jugemkey.jp/api/horoscope/free/'+ date)
    print(json.dumps(json.loads(res.text), indent=4, ensure_ascii=False))

    holo_def=[
            ["牡羊座","牡羊","おひつじざ","おひつじ座","おひつじ"],
            ["牡牛座","牡牛","おうしざ","おうし座","おうし"],
            ["双子座","双子","ふたござ","ふたご座","ふたご"],
            ["蟹座","蟹","かにざ","かに座","かに"],
            ["獅子座","獅子","かにざ","かに座","かに"],
            ["乙女座","乙女","おとめざ","おとめ座","おとめ"],
            ["天秤座","天秤","てんびんざ","てんびん座","てんびん"],
            ["蠍座","蠍","さそりざ","さそり座","さそり"],
            ["山羊座","山羊","やぎざ","やぎ座","やぎ"],
            ["牡牛座","牡牛","おうしざ","おうし座","おうし"],
            ["水瓶座","水瓶","みずがめざ","みずがめ座","みずがめ"],
            ["魚座","魚","うおざ","うお座","うお"],
            ]
    target_index = -1
    content = ""
    sign = ""
    reply_message = ""

    for i,d in enumerate(holo_def):
        if text in d:
            target_index = i

    if target_index > -1:
        content = res.json()["horoscope"][date][0]["content"]
        sign = res.json()["horoscope"][date][0]["sign"]
        reply_message = "{}のあなたの今日の運勢は,{}".format(sign,content)
    else:
        content = "占い結果が取得できませんでした"
        sign = text
        reply_message = "{}の{}".format(sign,content)
    #app.logger.info("Request text: " + txt)
    return reply_message


if __name__=="__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)