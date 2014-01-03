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

    urls = {prepareUrl(url) : url for url in urls if not is4chan(url)}

    f = open(folder + "/links.txt","r")
    lines = f.readlines()
    f.close()

    timestamp = str(int(time()))

    response = []
    for index, line in enumerate(lines):
        if not urls:
            break
        data = line.rstrip().split(" ")
        found = None
        for prepUrl, url in urls.iteritems():
            if (data[1] != prepUrl):
                continue
            count = int(data[2])
            countStr = "(x" + str(count) + ")" if count > 1 else ""
            nick = "<" + data[3] + ">"
            firstTime = datetime.fromtimestamp(int(data[4])).strftime("%d/%m/%Y %H:%M:%S")
            response.append("old!!! " + countStr + " Algselt linkis " + nick + " " + firstTime)
            lines.remove(line)
            lines.append(buildLine(data[0], data[1], count + 1, data[3], data[4], timestamp))
            found = prepUrl
        if found is not None:
            del urls[found]
    f = open(folder + "/links.txt","w")
    for line in lines:
        f.write(line)
    for prepUrl, url in urls.iteritems():
        line = buildLine(url[0], prepUrl, 1, author, timestamp, timestamp)
        f.write(line)
    f.close()
    return response

def buildLine(prefix, url, count, nick, firstTimestamp, lastTimestamp):
    count = str(count)
    return prefix + " " + url + " " + count + " " + nick + " " + firstTimestamp + " " + lastTimestamp + "\n"

def is4chan(url):
    return "4chan.org" in url[1]

def prepareUrl(url):
    url = url[1]
    youtubeUrl = re.findall(youtubeUrlRe, url)
    if (youtubeUrl):
        return youtubeUrl[0][1]
    if url[-1:] == "/":
        url = url[:-1]
    return url
