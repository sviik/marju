#!/opt/csw/bin/python
# coding=utf-8

import conf.config as config
from urllib import urlopen
from xml.dom.minidom import parseString

def getInfo():
    return "!fml - Suvaline postitus saidilt fmylife.com"

def get(parameter, channel):
    url = "http://api.fmylife.com/view/random/?key=" + config.FML_KEY + "&language=en"
    content = urlopen(url).read()
    dom = parseString(content)
    text = dom.getElementsByTagName('text')[0]
    value = text.firstChild.nodeValue.encode("utf-8")
    return value
