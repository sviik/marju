#!/opt/csw/bin/python
# coding=utf-8

import re
import fileinput
from time import time
from datetime import datetime

urlRe = re.compile('(http://www\.|https://www\.|http://|https://|www\.)(?P<link>\S+)')
youtubeUrlRe = re.compile('(youtube\.com/watch\?v=|youtube\.com/watch\?.*&v=|youtu.be/)(?P<id>[A-Za-z0-9_-]{11})')

def getResponseType():
    return "MSG"

def get(msg, author, folder):
    urls = re.findall(urlRe, msg)
    if (not urls):
        return
    urls = [prepareUrl(url) for url in urls if not is4chan(url)]
    urls = list(set(urls))

    f = open(folder + "/links.txt","r")
    lines = f.readlines()
    f.close()

    response = []
    for index, line in enumerate(lines):
        if not urls:
            break;
        data = line.rstrip().split(" ")
        found = None
        for url in urls:
            if (data[0] != url):
                continue
            count = int(data[1])
            countStr = "(x" + str(count) + ")" if count > 1 else ""
            nick = "<" + data[2] + ">"
            firstTime = datetime.fromtimestamp(int(data[3])).strftime("%d/%m/%Y %H:%M:%S")
            response.append("old!!! " + countStr + " Algselt linkis " + nick + " " + firstTime)
            lines[index] = buildLine(data[0], count + 1, data[2], data[3])
            found = url
        if found is not None:
            urls.remove(found)
    f = open(folder + "/links.txt","w")
    for line in lines:
        f.write(line)
    for url in urls:
        timestamp = str(int(time()))
        line = buildLine(url, 1, author, timestamp)
        f.write(line)
    f.close()
    return response

def buildLine(url, count, nick, timestamp):
    count = str(count)
    return url + " " + count + " " + nick + " " + timestamp + "\n"

def is4chan(url):
    return "4cdn.org" in url[1]

def prepareUrl(url):
    url = url[1]
    youtubeUrl = re.findall(youtubeUrlRe, url)
    if (youtubeUrl):
        return youtubeUrl[0][1]
    if url[-1:] == "/":
        url = url[:-1]
    return url