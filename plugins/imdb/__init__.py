#!/opt/csw/bin/python
# coding=utf-8

import json
from urllib import urlopen

def getInfo():
    return "!imdb [Filmi nimi] - Tagastab filmi nime, aasta, hinde ja IMDB lingi"

def get(parameter, channel):
    title = parameter.replace(' ', '+')
    url = "http://www.imdbapi.com/" + "?t=" + title
    r = urlopen(url).read()
    response = json.loads(r)
    if (response['Response'] == "True"):
        title = response["Title"].encode("utf-8")
        id = response["imdbID"].encode("utf-8")
        year = response["Year"].encode("utf-8")
        rating = response["imdbRating"].encode("utf-8")
        return title + " (" + year + ") [" + rating + "] http://www.imdb.com/title/" + id + "/";
    else:
        return "Ei leidnud seda filmi"