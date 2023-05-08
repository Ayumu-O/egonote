import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    TextSendMessage,
)

handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))


def lambda_handler(event, context):
    line_bot_api.broadcast(
        messages=TextSendMessage(
            text='お仕事お疲れ様です！\n今日の「できたこと」を 1 ~ 3 つ教えてください！'
        )
    )
