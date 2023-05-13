import os
import random

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    CarouselColumn,
    CarouselTemplate,
    MessageEvent,
    PostbackTemplateAction,
    TemplateSendMessage,
    TextMessage,
    TextSendMessage,
)

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
            "駅でエスクレーターではなく階段を使った",
            "朝に3キロ走った",
            "1日中子供とサッカーをした",
            "ヘルシーなお弁当を作った",
            "いつもより野菜を多く食べた",
            "いつも食べていない朝食を食べて出かけた",
            "先輩に悩みを相談し、本音を話せた",
            "有休を取って、ゆっくりできた",
        ]
    },
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
    input_text = event.message.text
    # reply_message = input_text

    reply = None
    if input_text == '例':
        reply = get_example_message()
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

def get_example_message():
    columns = []
    for column in EXAMPLES:
        examples_txt = '\n'.join(
            list(map(lambda x: f'・ {x}', column['examples']))
        )
        category = column['category']
        txt = f'{category}の例はこちらです！\n{examples_txt}'

        carousel = CarouselColumn(
            # thumbnail_image_url=column['thumbnail_image_url'],
            title=column['category'],
            text=column['category'],
            actions=[
                PostbackTemplateAction(
                    label='例を見る',
                    data=txt,
                )
            ]
        )
        columns.append(carousel)

    messages = TemplateSendMessage(
        alt_text='template',
        template=CarouselTemplate(columns=columns),
    )

    return messages


'''
時間に関するできたこと
- 旅行の1週間前に準備が終わった
- 納期通り商品を出荷できた
- 初めてアポイントが取れた
- いつもより30分早く会社に着いた
- 3分ぴったりでスピーチが終わった
- 1年ぶりに友達に会えた

数値に関するできたこと
- リスニングの点数が10点上がった
- 商談をいつもより３件多くこなした
- いつもより10ページ多く本を読んだ

習慣化に関するできたこと
- 通勤時に英語のリスニング教材を1ヶ月間聴き続けた
- 毎朝ランニングを3週間続けた
- 新聞を2ヶ月間、毎朝欠かさずに読んだ

人に感謝されたこと
- 読んで面白かった本の話をしたら、後輩にお礼を言われた
- 共有の場所をさっと掃除しておいたら、みんさんに感謝された
- 宴会の感じを引き受けたら感謝された
- 議事録を取っておいたら先輩に「ありがとう」と言ってもらえた

人に喜んでもらえたこと
- 他愛無い話で友達が笑ってくれた
- 同期の服装を褒めたら笑顔になった
- プレゼントを贈ったら喜んでもらえた

人にしてもらえたこと
- 商談の終わりに、相手に握手を求められた
- 真剣に話を聞いたら、友達がランチを奢ってくれた
- 相手の要望に近い価格を提示したら、玄関まで送ってもらえた
'''
