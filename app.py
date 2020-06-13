# -*- coding: utf-8 -*-
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel access token (long-lived)
line_bot_api = LineBotApi('LTXOF9UjoxKg90q3iixQCXW79qPm0r14fCErLlChybO5hdo5W7FmMwRPJthlmhdLL8riVZT8qggncxL1QfvZxJ1Itd/sIlw2RzR8qVapSuodpwWAF7zKOsNV6tU1Ra87OASC5STz798fA/mhhAOa3wdB04t89/1O/w1cDnyilFU=')

# Channel secret 
handler = WebhookHandler('68de8b5333de6824887c4b0e27dc79c4')


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

def movie():
    target_url = 'http://www.atmovies.com.tw/movie/next/0/'
    print('Start parsing movie ...')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('ul.filmListAll a')):
        if index == 20:
            break
        title = data.text.replace('\t', '').replace('\r', '')
        link = "http://www.atmovies.com.tw" + data['href']
        content += '{}\n{}\n'.format(title, link)
    return content



def getNews():
	"""
	建立一個抓最新消息的function
	"""
	import requests
	import re
	from bs4 import BeautifulSoup

	url = 'https://www.ettoday.net/news/focus/3C%E5%AE%B6%E9%9B%BB/'
	r = requests.get(url)
	reponse = r.text

	url_list = re.findall(r'<h3><a href="/news/[\d]*/[\d]*.htm" .*>.*</a>',reponse)

	soup = BeautifulSoup(url_list[0])
	url = 'https://fashion.ettoday.net/' + soup.find('a')['href']
	title = soup.text


	tmp = title + ': ' +url
	return tmp
	
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 傳送文字    
    if event.message.text.startswith('貼圖'):
        text = event.message.text
        _, package_id, sticker_id = text.split('-')
        message = StickerSendMessage(
            package_id=int(package_id),
            sticker_id=int(sticker_id)
        )
    elif event.message.text == '傳送文字':
        message = TextSendMessage(getNews())
    elif event.message.text == '傳送電影:
        message = TextSendMessage(moive())
	else:
        message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

	
if __name__ == '__main__':
    app.run(debug=True)