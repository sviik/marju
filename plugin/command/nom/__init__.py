#!/opt/csw/bin/python
# coding=utf-8

import re
from urllib import urlopen

paevapraedRe = re.compile('<p class="food" id="(TRUFFE|VILDE|PIERRE|POLPO|UT)_FOOD">(.+?)</p>', re.DOTALL)

def getCommands():
    return ["nom"]

def getInfo():
    return "Kokkuvõte tänastest Tartu restoranide päevapakkumistest"

def getResponseType():
    return "MSG"

def get(parameter, channel, author, folder):
    result = []
    matches = re.findall(paevapraedRe, urlopen("http://www.paevapraed.com").read())
    if (matches):
        for match in matches:
            info = match[0] + ": " + match[1].replace("<br/>", "; ").replace("<br />", "; ")
            info = (data[:150] + '...') if len(data) > 150 else data
            result.append(info)
    result.append('VAGAMAMA: nuudlid')
    return result