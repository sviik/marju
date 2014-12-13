#!/opt/csw/bin/python
# coding=utf-8

import json
from urllib import urlopen, urlencode

def getCommands():
    return ["imdb"]

def getInfo():
    return "[filmi nimi] Tagastab filmi nime, aasta, hinde ja IMDB lingi"

def getResponseType():
    return "MSG"

def get(parameter, channel, author, folder):
    params = {'t': parameter, 'plot': 'short'}
    url = "http://www.imdbapi.com/?" + urlencode(params)
    r = urlopen(url).read()
    response = json.loads(r)
    if (response['Response'] == "True"):
        title = response["Title"].encode("utf-8")
        id = response["imdbID"].encode("utf-8")
        year = response["Year"].encode("utf-8")
        rating = response["imdbRating"].encode("utf-8")
        plot = response["Plot"].encode("utf-8")
        if plot is not "":
            plot = "- " + plot
        return title + " (" + year + ") [" + rating + "] http://www.imdb.com/title/" + id + "/ " + plot
    else:
        return "Ei leidnud seda filmi"