# coding:utf-8

from boto3.session import Session
import os
import json
import boto3
import requests
from datetime import datetime
import pytz
from my_aws_utils import store_json_to_s3,get_json_from_s3


def lambda_handler(event, context):
    source = event['Records'][0]['s3']['object']['key']
    #source = 'forecast_130010.json'
    city_code = source[len('forecast_'):-5]  #キー名から、city_codeを抽出。temperature_130010.json → 130010
    bucket_name = event['Records'][0]['s3']['bucket']['name']

    json_data = get_json_from_s3(bucket_name, source)
    print(bucket_name)
    print(city_code)
    #print(key)
    #print(json_data)
    create_temperature_info_list(bucket_name,city_code,json_data)


def create_temperature_info_list(bucket_name,cityCode,json_data):
    '''
    以下、本当の処理。
    '''
    try:
        data0 = get_temperature_info(json_data,0)
        data1 = get_temperature_info(json_data,1)
        print(data0)
        print(data1)

        temp_series = []
        file = 'temperature_' + cityCode + '.json'
        if(exists(bucket_name,file)):
            print("exist");
            temp_series = get_json_from_s3('nu.mine.kino.temperature',file)

        '''
        自分と異なる日付のデータをとってきて、自分をAppend。
        '''
        if(is_replace_data(data0)):
            fResults0 = replace_temperature_info(data0,temp_series)
        else:
            fResults0 = temp_series
        if(is_replace_data(data1)):
            fResults1 = replace_temperature_info(data1,fResults0)
        else:
            fResults1 = fResults0

        result = json.dumps(fResults1, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
        store_json_to_s3('nu.mine.kino.temperature', file, result)
    except Exception as e:
        print(file + 'の処理でエラーが発生しました。')
        print(e)


def is_replace_data(target):
    return target['temperature']['max']!= None and target['temperature']['min']!= None


def replace_temperature_info(target,list):
    '''
    自分と異なる日付のデータをとってきて、自分をAppend。
    '''
    target_date = target['date']
    filtered_results = [item  for item in list if item['date'] != target_date]
    filtered_results.append(target)
    return filtered_results

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

    # 天気情報自体の更新日付
    originalUpdateDate = weatherjson['publicTime']

    return {
        'date':dateStr,
        'updateDate':updateDateStr,
        'originalUpdateDate': originalUpdateDate,
        'temperature':{
            'min':min,
            'max':max
        }
    }

if __name__ == "__main__":
    lambda_handler('', '')
    # create_temperature_info_list()
