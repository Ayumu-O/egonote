import os
import random

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))


def lambda_handler(event, context):
    headers = event["headers"]
    body = event["body"]

    # get X-Line-Signature header value
    signature = headers['x-line-signature']

    # handle webhook body
    handler.handle(body, signature)

    return {"statusCode": 200, "body": "OK"}


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    """ TextMessage handler """
    input_text = event.message.text
    # reply_message = input_text

    reply_message = ''
    if input_text == '例':
        reply_message = get_example()
    else:
        reply_messages = [
            'すごいですね！',
            'よかったですね！',
            'がんばりましたね！',
            'その調子です！',
        ]
        reply_message = reply_messages[
            random.randint(0, len(reply_messages) - 1)
        ]

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message))

def get_example():
    return 'これは例です'
