#!/opt/csw/bin/python
# coding=utf-8

import conf.config as config
from urllib import urlopen, urlencode
from xml.dom.minidom import parseString

def getCommands():
    return ["fml"]

def getResponseType():
    return "MSG"

def getInfo():
    return "Suvaline postitus saidilt fmylife.com"

def get(parameter, channel, author, folder):
    params = {'key': config.FML_KEY, 'language': 'en'}
    url = "http://api.fmylife.com/view/random/?" + urlencode(params)
    content = urlopen(url).read()
    dom = parseString(content)
    text = dom.getElementsByTagName('text')[0]
    value = text.firstChild.nodeValue.encode("utf-8")
    return value
