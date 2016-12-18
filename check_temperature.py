# coding:utf-8

from boto3.session import Session

import json
import ConfigParser
import boto3
import pytz
from datetime import datetime, timedelta
from my_aws_utils import store_json_to_s3, get_json_from_s3


config = ConfigParser.SafeConfigParser()
config.read('./config/config.ini')

def lambda_handler(event, context):
    bucket_name = 'nu.mine.kino.temperature'
    source = 'temperature_130010.json'
    json_data = get_json_from_s3(bucket_name, source)

    jst = pytz.timezone('Asia/Tokyo')
    today = datetime.now(tz=jst)

    today_str = today.strftime('%Y-%m-%d')
    yesterday_str = (today + timedelta(days=-1)).strftime('%Y-%m-%d')

    today_data = [item for item in json_data if item['date'] == today_str][0]
    yesterday_data = [item for item in json_data if item['date'] == yesterday_str][0]

    today_data_str = json.dumps(today_data['temperature'])
    yesterday_data_str = json.dumps(yesterday_data['temperature'])



    send_message = '気温情報\n\n'
    send_message += today_str+' :' + today_data_str + ' ave:' +str(mean([today_data['temperature']['max'],today_data['temperature']['min']])) + '\n'
    send_message += yesterday_str+' :' + yesterday_data_str + ' ave:' + str(mean([yesterday_data['temperature']['max'],yesterday_data['temperature']['min']])) + '\n'
    topic = config.get('aws', 'topic')
    subject = today_str + ' の気温情報'

    print(send_message)

    sns = boto3.client('sns')
    response = sns.publish(
        TopicArn=topic,
        Message=send_message,
        Subject=subject,
        MessageStructure='Raw'
    )


def sum(a):
    s = 0.0
    for x in a:
        s += x
    return s


def mean(a):
    return sum(a) / len(a)


def var(a, ddof=0):
    m = mean(a)
    v = 0.0
    for x in a:
        v += (x - m) ** 2
    return v / (len(a) - ddof)







if __name__ == "__main__":
    lambda_handler('', '')
