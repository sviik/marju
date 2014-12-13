#!/opt/csw/bin/python
# coding=utf-8

import re
from urllib import urlopen

paevapraedRe = re.compile('<p class="food" id="(TRUFFE|VILDE|FEELGOOD|POLPO|UT)_FOOD">(.+?)</p>', re.DOTALL)
noirRe = re.compile('<div class="article-box.+?location = \'(.+?)\'">')
noirArticleRe = re.compile('<div class="content-texts-wrapper.+?<h1>(.+?)<span.+?>(.+?)</span.+?<h2>(.+?)</h2>', re.DOTALL)

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
            result.append(match[0] + ": " + match[1].replace("<br/>", "; ").replace("<br />", "; "))
    result.append('VAGAMAMA: nuudlid')
    return result