#!/opt/csw/bin/python
# coding=utf-8

from urllib import urlopen, urlencode
import re
import json
import conf.config as config

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
        params = {'id': id, 'key': config.GOOGLE_KEY, 'fields': 'items(snippet(title))', 'part' : 'snippet'}
        url = 'https://www.googleapis.com/youtube/v3/videos?' + urlencode(params)
        result = json.loads(urlopen(url).read())
        if ('error' in result):
            continue
        title = result['items'][0]['snippet']['title'].encode("utf-8")
        response.append(title)
    return response
