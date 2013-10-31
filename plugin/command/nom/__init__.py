#!/opt/csw/bin/python
# coding=utf-8

import re
from urllib import urlopen

paevapraedRe = re.compile('<p class="food" id="(PREMIUM|TRUFFE|VAGAMAMA|FEELGOOD|POLPO)_FOOD">(.+?)</p>', re.DOTALL)
noirRe = re.compile('<div class="article-box.+?location = \'(.+?)\'">')
noirArticleRe = re.compile('<div class="content-texts-wrapper.+?<h1>(.+?)<span.+?>(.+?)</span.+?<h2>(.+?)</h2>', re.DOTALL)

def getInfo():
    return "!nom - Kokkuvõte tänastest Tartu restoranide päevapakkumistest"

def getResponseType():
    return "MSG"

def get(parameter, channel, author, folder):
    result = []
    link = re.search(noirRe, urlopen("http://www.cafenoir.ee").read())
    if (link):
        noirNom = re.search(noirArticleRe, urlopen("http://www.cafenoir.ee" + link.group(1)).read())
        if (noirNom):
            result.append("NOIR: " + noirNom.group(1).strip(' \t\n\r') + "; " + noirNom.group(3).strip(' \t\n\r') + " (" + noirNom.group(2).strip(' \t\n\r') + ")")

    matches = re.findall(paevapraedRe, urlopen("http://www.paevapraed.com").read())
    if (matches):
        for match in matches:
            result.append(match[0] + ": " + match[1].replace("<br/>", "; ").replace("<br />", "; "))

    return result