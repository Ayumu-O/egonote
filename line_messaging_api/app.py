# --- coding: utf-8 ---
import logging
import os
import random

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    CarouselColumn,
    CarouselTemplate,
    MessageEvent,
    PostbackEvent,
    PostbackTemplateAction,
    TemplateSendMessage,
    TextMessage,
    TextSendMessage,
)

from example import EXAMPLES

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

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
    logger.info('Received text message.')
    logger.info(event)

    input_text = event.message.text
    # reply_message = input_text

    reply = None
    if input_text == '例':
        reply = get_example_carousels()
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
        reply = TextSendMessage(text=reply_message)

    logger.info(reply)

    line_bot_api.reply_message(
        event.reply_token,
        reply
    )


@handler.add(PostbackEvent)
def handle_post_back(event):
    """PostbackEvent handler"""
    logger.info('Received text message.')
    logger.info(event)

    input_data = event.postback.data

    key, value = input_data.split("=")
    message = None
    if key == "example_category":
        for exam in EXAMPLES:
            category = exam['category']
            if value == category:
                examples_txt = '\n'.join(
                    list(map(lambda x: f'・ {x}', exam['examples']))
                )
                txt = f'{category}の例はこちらです！\n{examples_txt}'
                message = TextSendMessage(text=txt)
                break

        logger.info(message)

        line_bot_api.reply_message(
            event.reply_token,
            message
        )


def get_example_carousels():
    columns = []
    for column in EXAMPLES:
        category = column['category']
        # examples_txt = '\n'.join(
        #     list(map(lambda x: f'・ {x}', column['examples']))
        # )
        carousel = CarouselColumn(
            # thumbnail_image_url=column['thumbnail_image_url'],
            title=category,
            text=category,
            actions=[
                PostbackTemplateAction(
                    label='例を見る',
                    data=f'example_category={category}',
                )
            ]
        )
        columns.append(carousel)

    messages = TemplateSendMessage(
        alt_text='template',
        template=CarouselTemplate(columns=columns),
    )

    logger.info(messages)

    return messages
