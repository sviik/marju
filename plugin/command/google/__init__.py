#!/opt/csw/bin/python
# coding=utf-8

from urllib import urlopen, urlencode
import json
import conf.config as config

def getCommands():
    return ["google", "g"]

def getInfo():
    return "!google [otsingufraas] - Google otsing"

def getResponseType():
    return "MSG"

def get(parameter, channel, author, folder):
    if (not parameter):
        return None
    params = {'key': config.GOOGLE_KEY, 'cx': config.GOOGLE_CX, 'num': 3, 'q': parameter}
    url = 'https://www.googleapis.com/customsearch/v1?' + urlencode(params)
    r = urlopen(url).read()
    response = json.loads(r)
    if (response['searchInformation']['totalResults'] == '0'):
        return 'Ei leidnud midagi'
    items = response['items']
    result = []
    for item in items:
        result.append(item['link'])
    return result