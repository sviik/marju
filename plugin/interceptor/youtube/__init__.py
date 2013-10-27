#!/opt/csw/bin/python
# coding=utf-8

from urllib import urlopen
import re
import json

youtubeUrlRe = re.compile('(youtube\.com/watch\?v=|youtube\.com/watch\?.*&v=|youtu.be/)(?P<id>[A-Za-z0-9_-]{11})')

def getResponseType():
    return "MSG"

def get(msg, author, folder):
    matches = re.findall(youtubeUrlRe, msg)
    if (not matches):
        return
    response = []
    for match in matches:
        id = match[1]
        url = 'http://gdata.youtube.com/feeds/api/videos/' + id + '?v=2&alt=jsonc'
        result = urlopen(url).read()
        info = json.loads(result)
        if ('error' in response):
            continue
        title = info['data']['title'].encode("utf-8")
        response.append(title)
    return response
