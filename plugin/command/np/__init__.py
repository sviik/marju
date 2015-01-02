#!/opt/csw/bin/python
# coding=utf-8

import json
from urllib import urlopen, urlencode
from conf import config

def getCommands():
    return ["np"]

def getResponseType():
    return "MSG"

def getInfo():
    return "[kasutajanimi] Tagastab last.fm-s hetkel mängiva loo"


class UserNotFoundError(BaseException):
    pass

def get(parameter, channel, author, folder):
    username = parameter
    if not username:
        return "Kasutajanimi on puudu"

    try:
        playingTrack = findPlayingTrack(username)
    except UserNotFoundError:
        return "Kasutajat ei leitud"

    if playingTrack:
        return formatPlayingTrack(playingTrack)

    return "%s ei kuula hetkel midagi" % username

def findPlayingTrack(username):
    tracks = getRecentTracks(username)
    if not tracks:
        return None
    for track in tracks:
        attributes = track.get('@attr')
        if attributes:
            if attributes.get('nowplaying', False):
                return track
    return None

def getRecentTracks(username):
    params = {'method': 'user.getrecenttracks', 'user': username, 'api_key': config.LASTFM_KEY, 'limit': '1', 'format': 'json'}
    url = "http://ws.audioscrobbler.com/2.0/?" + urlencode(params)
    content = urlopen(url).read()
    data = json.loads(content)
    if "error" in data and data["error"] == 6:
        raise UserNotFoundError
    recentTracks = data.get('recenttracks')
    if not recentTracks:
        return []
    trackEntry = recentTracks.get('track')
    # Response might be a dict or a list, make a list of it either way
    return [trackEntry] if type(trackEntry) == dict else trackEntry

def formatPlayingTrack(track):
    album = track.get('album')
    artist = track.get('artist')
    return "%s - %s (%s)" % (artist.get('#text').encode("utf-8"), track.get('name').encode("utf-8"), album.get('#text').encode("utf-8"))
