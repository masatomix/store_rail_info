# coding:utf-8

from boto3.session import Session
import os
import json
import datetime
import boto3
import requests
from myutils import contains


def get_json_from_s3(bucket_name, key):
    '''
    if (os.path.exists(key) == True):
        with open(key) as data_file:
            results = json.load(data_file)
            return results
    return None
    '''

    s3 = boto3.resource('s3')
    #bucket = s3.Bucket(bucket_name)
    #obj = bucket.Object('delay.json')
    obj = s3.Object(bucket_name, key)
    response = obj.get()
    body = response['Body'].read()
    return json.loads(body.decode('utf-8'))



def store_json_to_s3(bucket_name, key, json_data):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    obj = bucket.Object(key)

    response = obj.put(
        Body=json_data.encode('utf-8'),
        ContentEncoding='utf-8',
        ContentType='application/json'
    )




def main():
    print(datetime.datetime.fromtimestamp(1479460502))


if __name__ == "__main__":
    main()
