# coding:utf-8

from boto3.session import Session
import os
import json
import boto3
import requests
from my_aws_utils import store_json_to_s3


# import itertools



def getCityCodes():
    #	r = requests.get('http://weather.livedoor.com/forecast/rss/primary_area.xml')

    returnList = []
    codes = createCityCodes()
    names = createCityNames()

    for i, code in enumerate(codes):
        #	for code,name in itertools.zip_longest(codes,names):
        returnObj = {
            'cityCode': code,
            'cityName': names[i]
        }
        returnList.append(returnObj)

    result = json.dumps(returnList, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    store_json_to_s3('nu.mine.kino.temperature', 'cityCodes.json', result)


def lambda_handler(event, context):
    # cityCode = '130010'
    # cityCodesResponse = requests.get('https://s3-ap-northeast-1.amazonaws.com/nu.mine.kino.temperature/cityCodes.json')
    getCityCodes()
    storeWeather(createCityCodes())


def storeWeather(cityCodes):
    for cityCode in cityCodes:
        q = {
            'city': cityCode
        }
        r = requests.get('http://weather.livedoor.com/forecast/webservice/json/v1', params=q)
        result = json.dumps(r.json(), ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
        file = 'forecast_' + cityCode + '.json'
        store_json_to_s3('nu.mine.kino.temperature', file, result)


# def storeJSON2S3(bucketName,key,jsonData):
# 	s3 = boto3.resource('s3')
# 	bucket = s3.Bucket(bucketName)
#
# 	obj = bucket.Object(key)
#
# 	response = obj.put(
# 		Body=jsonData.encode('utf-8'),
# 		ContentEncoding='utf-8',
# 		ContentType='application/json'
# 	)


def createCityNames():
    return [
        'さいたま',
        '千葉',
        '東京',
        '横浜',
        '長野',
        '福岡',
        '那覇',
        '宮古島',
        '石垣島',
    ]


def createCityCodes():
    return [
        '110010',
        '120010',
        '130010',
        '140010',
        '200010',
        '400010',
        '471010',
        '473000',
        '474010',
    ]


if __name__ == "__main__":
    lambda_handler('', '')
# getCityCodes()
