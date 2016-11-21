# coding:utf-8

from boto3.session import Session
import os
import json
import boto3
import requests
from myutils import contains
from my_aws_utils import store_json_to_s3


# ネットから情報を取得し、S3へストアする。指定した路線だけに絞って、ストアすることにした。
def lambda_handler(event, context):
    q = {}
    r = requests.get('https://rti-giken.jp/fhc/api/train_tetsudo/delay.json', params=q)

    jsonData = r.json()
    result = json.dumps(jsonData, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

    filteredJsonData = filter(jsonData, createRailTargets())
    store_json_to_s3('nu.mine.kino.temperature', 'delay.json', filteredJsonData)



def filter(jsonData, targets):
    targets = createRailTargets()

    list = []
    for element in jsonData:
        if contains(element['name'], targets):
            list.append(element)
    return json.dumps(list, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


def createRailTargets():
    return [
        #		'豊肥本線',
        #		'根室本線',
        '東横線',  #
        '東海道線',  #
        '中央線快速電車',  #
        '湘南新宿ライン',  #
        '丸ノ内線',
        '日比谷線',
        '東西線',
        '千代田線',
        '有楽町線',
        '半蔵門線',
        '南北線',
        '副都心線',
        '山手線',
        '京浜東北線',
        '京王線',
        '浅草線',
        '三田線',
        '新宿線',
        '大江戸線',
        '都営新宿線',
        '小田急線',
        '横須賀線',
        '南武線',
        '中央･総武各駅停車',
        '総武快速線',
        # '中央本線',
        '総武本線',
        '高崎線',
        '京葉線',
        '東京モノレール',
        'りんかい線',
        '京急線',
        '相鉄線',
        '東急線',
        '横浜市営地下鉄',
        'ゆりかもめ',
        '埼京線',
    ]


if __name__ == "__main__":
    lambda_handler('', '')
