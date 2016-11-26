# coding:utf-8

from boto3.session import Session
import os
import json
#import datetime
from datetime import datetime, timedelta
import pytz
import boto3
import requests
from myutils import contains
from my_aws_utils import store_json_to_s3,get_json_from_s3


bucket_name = 'nu.mine.kino.temperature'


# ネットから情報を取得し、S3へストアする。指定した路線だけに絞って、ストアすることにした。
def lambda_handler(event, context):
    delayList = get_json_from_s3(bucket_name, 'delay.json')
    delayPrevList = get_json_from_s3(bucket_name, 'delay_prev.json')

    if (compare(delayList, delayPrevList)):
        print('DIFFなし')
        #message = '電車運行情報で更新情報なし'
        #send_mail(message,delayList,delayPrevList)
    else:
        print('DIFFアリ')
        message = '電車運行情報で更新情報あり'
        send_mail(message, delayList, delayPrevList)

    # 直近のファイルを、前回分として保存。(次回のため)
    result = json.dumps(delayList, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    store_json_to_s3(bucket_name, 'delay_prev.json', result)


def send_mail(message, delayList, delayPrevList):
    send_message = '電車運行情報\n\n'

    jst = pytz.timezone('Asia/Tokyo')

    for i, obj in enumerate(delayList):
        update_time = datetime.fromtimestamp(obj['lastupdate_gmt'],tz=jst)
        send_message += '・%s (%s)\n' % (obj['name'], update_time.strftime("%H:%M"))

    send_message += '\n'
    send_message += '(カッコは更新時刻)\n'
    send_message += 'https://www.tetsudo.com/traffic/\n'
    send_message += 'https://rti-giken.jp/fhc/api/train_tetsudo/\n'

    send_message += '\n\n\n\n------------------\n'
    send_message += 'delayList\n'
    send_message += '------------------\n'

    for i, obj in enumerate(delayList):
        send_message += json.dumps(obj, ensure_ascii=False) + '\n'

    send_message += '\n'

    send_message += 'delayPrevList\n'
    send_message += '------------------\n'

    for i, obj in enumerate(delayPrevList):
        send_message += json.dumps(obj, ensure_ascii=False) + '\n'

    send_message += '------------------\n'
    topic = 'arn:aws:sns:ap-northeast-1:xxxxxxxxxxxx:xxxxxxx'
    subject = message
    region = 'ap-northeast-1'

    sns = boto3.client('sns')
    response = sns.publish(
        TopicArn=topic,
        Message=send_message,
        Subject=subject,
        MessageStructure='Raw'
    )


def compare(delayList, delayPrevList):
    #    print(delayList)
    #    print(delayPrevList)
    for i, obj in enumerate(delayList):
        print(obj)
    print('------------------')
    for i, obj in enumerate(delayPrevList):
        print(obj)
    print('------------------')

    # サイズ違いはそもそもDIFFあり
    if (len(delayList) != len(delayPrevList)):
        return False

    # サイズがおなじ場合、now側で、For文回す
    for i, delay in enumerate(delayList):
        print(delay['name'], ' で処理開始')
        matchFlag = containsRailInfo(delay,delayList)

        # 一つづつもってきて、名前があるかを比較
        #for delayPrev in delayPrevList:
        #    matchFlag = compareRailInfo(delay,delayPrev)

        # containsRailInfo をくぐり抜けて、Falseだったら 一致するものがなかったということ
        if (not (matchFlag)):
            return False

    return True


def compareRailInfo(a,b):
    '''
    引数のRailInfoオブジェクトを比較する。name 属性がおなじかどうか。
    :param a:
    :param b:
    :return:
    '''
    return a['name']==b['name']


def containsRailInfo(target,list):
    '''
    引数のRailInfoオブジェクトを比較する。含まれているかどうかをTrue/Falseで。
    :param target:
    :param list:
    :return:
    '''
    for element in list:
        if(compareRailInfo(target,element)):
            return True
    return False




def main():
    jst = pytz.timezone('Asia/Tokyo')
    print(datetime.fromtimestamp(1479460502))
    date = datetime.fromtimestamp(1479460502,tz=jst)
    print(date)
    print(date.strftime("%Y/%m/%d %H:%M:%S"))
    a_test()


def a_test():
    jsonStr1 = '''
    {
        "lastupdate_gmt": 1479471904,
        "name": "京急線",
        "company": "京急電鉄",
        "source": "鉄道com RSSa"
    }
    '''
    jsonStr2 = '''
    [
        {
            "company": "都営地下鉄",
            "lastupdate_gmt": 1479472082,
            "name": "浅草線",
            "source": "鉄道com RSS"
        },
        {
            "company": "京急電鉄",
            "lastupdate_gmt": 1479471904,
            "name": "京急線",
            "source": "鉄道com RSS"
        }
    ]
    '''


    target = json.loads(jsonStr1)
    list = json.loads(jsonStr2)

    print(containsRailInfo(target,list))




if __name__ == "__main__":
    #lambda_handler('','')
    main()
