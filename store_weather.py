# coding:utf-8

from boto3.session import Session
import os
import json
import boto3
import requests
from datetime import datetime
import pytz
from my_aws_utils import store_json_to_s3,get_json_from_s3


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
        createTemp('nu.mine.kino.temperature', cityCode, r.json())


def createTemp(bucket_name, cityCode, json_data):
    try:
        temp_series = []
        file = 'temperature_' + cityCode + '.json'
        if(not(exists(bucket_name,file))):
            print("not exists");
        else:
            print("exist");
            temp_series = get_json_from_s3('nu.mine.kino.temperature',file)
            # get_json_from_s3('nu.mine.kino.temperature',file)

        data0 = get_temperature_info(json_data,0)
        data1 = get_temperature_info(json_data,1)
        print(data0)
        print(data1)
        temp_series.append(data0)
        temp_series.append(data1)

        result = json.dumps(temp_series, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
        store_json_to_s3('nu.mine.kino.temperature', file, result)
    except Exception as e:
        print(file + 'の処理でエラーが発生しました。')
        print(e)



def exists(bucket_name, key) :
    s3client = Session().client('s3')
    return 'Contents' in s3client.list_objects(Prefix=key, Bucket=bucket_name)



def get_temperature_info(weatherjson,index):
    dateStr = weatherjson['forecasts'][index]['date']
    temp = weatherjson['forecasts'][index]['temperature']

    min = None
    max = None

    if(temp['min'] != None):
        min = temp['min']['celsius']
    if(temp['max'] != None):
        max = temp['max']['celsius']

    jst = pytz.timezone('Asia/Tokyo')
    updateDateStr = datetime.now(tz=jst).strftime('%Y/%m/%d %H:%M')

    return {
        'date':dateStr,
        'updateDate':updateDateStr,
        'temperature':{
            'min':min,
            'max':max
        }
    }



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
