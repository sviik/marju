#!/opt/csw/bin/python
# coding=utf-8

from datetime import timedelta
from urllib import urlopen
import re
import json

trackRe = re.compile('(spotify:track:)(?P<id>[A-Za-z0-9]{22})')
#albumRe = re.compile('(spotify:album:)(?P<id>[A-Za-z0-9]{22})')
#artistRe = re.compile('(spotify:artist:)(?P<id>[A-Za-z0-9]{22})')


def getResponseType():
    return "MSG"

def get(msg, author, folder):
    matches = re.findall(trackRe, msg)
    if (not matches):
        return
    response = []
    for match in matches:
        id = match[1]
        url = 'https://api.spotify.com/v1/tracks/' + id
        result = urlopen(url).read()
        info = json.loads(result)
        if ('error' in info):
            continue
        artist = getArtist(info)
        name = getName(info)
        duration = getDuration(info)
        response.append(artist + " - " + name + " [" + duration + "]")
    return response

def getArtist(info):
    artists = info["artists"]
    return artists[0]["name"].encode("utf-8")

def getName(info):
    return info["name"].encode("utf-8")

def getDuration(info):
    duration_ms = info["duration_ms"]
    td = str(timedelta(seconds=duration_ms/1000))
    if (td[:2] == "0:"):
        td = td[2:]
    return td