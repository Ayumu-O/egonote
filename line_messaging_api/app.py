# --- coding: utf-8 ---
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

import json
import logging
import traceback

# class FormatterJSON(logging.Formatter):
#     def format(self, record):
#         if self.usesTime():
#             record.asctime = self.formatTime(record, self.datefmt)
#         j = {
#             'logLevel': record.levelname,
#             'timestamp': '%(asctime)s.%(msecs)dZ' % dict(asctime=record.asctime, msecs=record.msecs),
#             'timestamp_epoch': record.created,
#             'aws_request_id': getattr(record, 'aws_request_id', '00000000-0000-0000-0000-000000000000'),
#             'message': record.getMessage(),
#             'module': record.module,
#             'filename': record.filename,
#             'funcName': record.funcName,
#             'levelno': record.levelno,
#             'lineno': record.lineno,
#             'traceback': {},
#             'extra_data': record.__dict__.get('extra_data', {}),
#             'event': record.__dict__.get('event', {}),
#         }
#         if record.exc_info:
#             exception_data = traceback.format_exc().splitlines()
#             j['traceback'] = exception_data
#         print(j)
#         return json.dumps(j, ensure_ascii=False)

class JsonFormatter:
    def format(self, record):
        print(record)
        return json.dumps(vars(record))

logging.basicConfig()
# formatter = FormatterJSON(
#     '[%(levelname)s]\t%(asctime)s.%(msecs)dZ\t%(levelno)s\t%(message)s\n',
#     '%Y-%m-%dT%H:%M:%S'
# )
# ローカル環境ではStreamHandlerが、AWS Lambdaでは元々存在しているLambdaHandlerがハンドラとしてセットされる
# https://ops.jig-saw.com/tech-cate/lambda-python-log
logging.getLogger().handlers[0].setFormatter(JsonFormatter())
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

EXAMPLES = [
    {
        'category': 'スッキリしたこと',
        'examples': [
            "机の上をきれいに片付けた",
            "たまっていた雑務を処理した",
            "顧客のクレームを解決した",
            "パソコン内のフォルダを整理した",
            "英単語帳を1冊終えた",
            "プログラムのバグをなくすことができた",
        ]
    },
    {
        'category': 'ワクワクしたこと',
        'examples': [
            "電話の対応が上手にできた",
            "会いたいと思っていた人に会えた",
            "レポートがうまく書けた",
            "家計簿の計算が一発でぴったり合った",
            "英会話でいつもよりうまく話せた",
            "新しいプロジェクトをスムーズにスタートできた",
        ]
    },
    {
        'category': 'ハツラツとしたこと',
        'examples': [
            "駅でエスカレーターではなく階段を使った",
            "朝に3キロ走った",
            "1日中子供とサッカーをした",
            "ヘルシーなお弁当を作った",
            "いつもより野菜を多く食べた",
            "いつも食べていない朝食を食べて出かけた",
            "先輩に悩みを相談し、本音を話せた",
            "有休を取って、ゆっくりできた",
        ]
    },
    {
        'category': '時間に関するできたこと',
        'examples': [
            '旅行の1週間前に準備が終わった',
            '納期通り商品を出荷できた',
            '初めてアポイントが取れた',
            'いつもより30分早く会社に着いた',
            '3分ぴったりでスピーチが終わった',
            '1年ぶりに友達に会えた',
        ]
    },
    {
        'category': '数値に関するできたこと',
        'examples': [
            'リスニングの点数が10点上がった',
            '商談をいつもより３件多くこなした',
            'いつもより10ページ多く本を読んだ',
        ]
    },
    {
        'category': '習慣化に関するできたこと',
        'examples': [
            '通勤時に英語のリスニング教材を1ヶ月間聴き続けた',
            '毎朝ランニングを3週間続けた',
            '新聞を2ヶ月間、毎朝欠かさずに読んだ',
        ]
    },
    {
        'category': '人に感謝されたこと',
        'examples': [
            '読んで面白かった本の話をしたら、後輩にお礼を言われた',
            '共有の場所をさっと掃除しておいたら、みんさんに感謝された',
            '宴会の感じを引き受けたら感謝された',
            '議事録を取っておいたら先輩に「ありがとう」と言ってもらえた',
        ]
    },
    {
        'category': '人に喜んでもらえたこと',
        'examples': [
            '他愛無い話で友達が笑ってくれた',
            '同期の服装を褒めたら笑顔になった',
            'プレゼントを贈ったら喜んでもらえた',
        ]
    },
    {
        'category': '人にしてもらえたこと',
        'examples': [
            '商談の終わりに、相手に握手を求められた',
            '真剣に話を聞いたら、友達がランチを奢ってくれた',
            '相手の要望に近い価格を提示したら、玄関まで送ってもらえた',
        ]
    }
]

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
    logger.info('Received text message', extra=event)
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

    line_bot_api.reply_message(
        event.reply_token,
        reply
    )


@handler.add(PostbackEvent)
def handle_post_back(event):
    """PostbackEvent handler"""
    logger.info({'event': vars(event)})
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

    return messages
