#!/opt/csw/bin/python
# coding=utf-8

from urllib import urlopen
import json
import conf.config as config

def getInfo():
    return "!google [otsingufraas] - Google otsing"

def get(parameter, folder):
        url = 'https://www.googleapis.com/customsearch/v1'
        key = config.GOOGLE_KEY
        cx = config.GOOGLE_CX
        num = '&num=3'
        query = '&q=' + parameter.replace(' ', '+')
        url = url + key + cx + num + query
        r = urlopen(url).read()
        response = json.loads(r)
        if (response['searchInformation']['totalResults'] == '0'):
            return 'Ei leidnud midagi'
        items = response['items']
        result = []
        for item in items:
            result.append(item['link'])
        return result