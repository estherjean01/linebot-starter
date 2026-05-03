from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# =====================================================
# ★ 請在下方兩個地方貼上你的金鑰 ★
# =====================================================

LINE_CHANNEL_SECRET = '720ec910eb066df4b6c88428b4ce2ab8'   # ← 貼在這裡
LINE_CHANNEL_ACCESS_TOKEN = 'hvMa5fFml7Woa0TD3MiyDCBBhAqV5onqHsoIJt65f+NRjU5P3IPmjgfxF55QmFDAve97J+V/wc0o++hn/RtUxUDpP4VgpNsXyUdXfNpKIEG0OKYy/hjn8E+pIfSLupohHtQnaTVQ4AyjvxoztY20zwdB04t89/1O/w1cDnyilFU=v'  # ← 貼在這裡

# =====================================================

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@app.route("/webhook", methods=['POST'])
def webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 取得使用者傳來的訊息
    user_msg = event.message.text

    # =====================================================
    # ★ 關鍵字回覆設定區（可以自由新增！） ★
    # =====================================================

    if '你好' in user_msg:
        reply = '哈囉！你好～ 😊'

    elif '天氣' in user_msg:
        reply = '今天天氣晴朗，出門記得防曬！☀️'

    elif '謝謝' in user_msg:
        reply = '不客氣！隨時都可以找我聊天 🙌'

    elif '早安' in user_msg:
        reply = '早安！今天也要加油喔 💪'

    elif '午安' in user_msg:
        reply = '午安！吃飽了嗎？記得午休一下 😴'

    elif '晚安' in user_msg:
        reply = '晚安～好好休息，明天見 🌙'

    elif '幫助' in user_msg or '你會什麼' in user_msg:
        reply = '你可以跟我說：你好、天氣、謝謝、早安、午安、晚安 😄'

    else:
        reply = '我還在學習中！你可以說「你好」或「幫助」試試看 🤖'

    # =====================================================

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )


if __name__ == "__main__":
    app.run()
