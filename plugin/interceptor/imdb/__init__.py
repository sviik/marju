#!/opt/csw/bin/python
# coding=utf-8

from urllib import urlopen, urlencode
import re
import json

imdbUrlRe = re.compile('(imdb\.com/title/(?P<id>tt[0-9]{7}))')

def getResponseType():
    return "MSG"

def get(msg, author, folder):
    matches = re.findall(imdbUrlRe, msg)
    if (not matches):
        return
    matches = list(set(matches))

    baseUrl = "http://www.omdbapi.com/?"
    movies = []
    for match in matches:
        params = {'i': match[1]}
        url = baseUrl + urlencode(params)
        r = urlopen(url).read()
        movies.append(json.loads(r))

    result = []
    for movie in movies:
        title = movie['Title'].encode("utf-8")
        year = " " + str(movie['Year']) if "Year" in movie else ""
        rating = "[" + str(movie['imdbRating']) + "] " if "imdbRating" in movie else ""
        plot = "- " + movie['Plot'].encode("utf-8") if "Plot" in movie else ""
        country = movie['Country'].encode("utf-8") if "Country" in movie else ""
        result.append(title + " (" + country + year + ") " + rating + plot)

    return result
