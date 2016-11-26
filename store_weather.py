# coding:utf-8

import json
import requests
from my_aws_utils import store_json_to_s3,get_json_from_s3
from store_temperature import get_temperature_info,exists


# import itertools

BUCKET_NAME = 'nu.mine.kino.temperature'

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
    store_json_to_s3(BUCKET_NAME, 'cityCodes.json', result)


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
        obj = r.json()
        result = json.dumps(obj, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
        file = 'forecast_' + cityCode + '.json'
        store_json_to_s3(BUCKET_NAME, file, result)

        createTemp(BUCKET_NAME, cityCode, obj)


def createTemp(bucket_name, cityCode, json_data):
    try:
        temp_series = []
        data0 = get_temperature_info(json_data,0)
        data1 = get_temperature_info(json_data,1)
        print(data0)
        print(data1)
        file = 'new_temperature_' + cityCode + '.json'
        if(exists(bucket_name,file)):
            print("exist");
            temp_series = get_json_from_s3(bucket_name,file)
        temp_series.append(data0)
        temp_series.append(data1)

        result = json.dumps(temp_series, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
        store_json_to_s3(bucket_name, file, result)
    except Exception as e:
        print(file + 'の処理でエラーが発生しました。')
        print(e)


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
