#!/opt/csw/bin/python
# coding=utf-8

import json
from urllib import urlopen
from conf import config


def getResponseType():
    return "MSG"


def getInfo():
    return "!np [kasutajanimi] - Tagastab last.fm-s hetkel mängiva loo"


def get(parameter, channel, author, folder):
    username = parameter.split(" ")[0]
    if not username:
        return "Kasutajanimeta ei saa näidata, mis laul mängib"

    playingTrack = findPlayingTrack(username)
    if playingTrack:
        return formatPlayingTrack(playingTrack)
    return "%s ei kuula hetkel midagi" % username


def findPlayingTrack(username):
    tracks = getRecentTracks(username)
    for track in tracks:
        attributes = track.get('@attr')
        if attributes:
            if attributes.get('nowplaying', False):
                return track
    return None


def getRecentTracks(username):
    url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=%s&api_key=%s&limit=1&format=json" % \
          (username, config.LASTFM_KEY)
    content = urlopen(url).read()
    data = json.loads(content)

    recentTracks = data.get('recenttracks')
    if not recentTracks:
        return []

    trackEntry = recentTracks.get('track')
    # Response might be a dict or a list, make a list of it either way
    return [trackEntry] if type(trackEntry) == dict else trackEntry


def formatPlayingTrack(track):
    album = track.get('album')
    artist = track.get('artist')
    return "%s - %s (%s)" % (artist.get('#text'), track.get('name'), album.get('#text'))
