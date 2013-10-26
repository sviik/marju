#!/opt/csw/bin/python
# coding=utf-8

from urllib import urlopen
import re
import json

imdbUrlRe = re.compile('(imdb\.com/title/(?P<id>tt[0-9]{7}))')

def do(msg, author, folder):
    matches = re.findall(imdbUrlRe, msg)
    if (not matches):
        return
    matches = list(set(matches))

    ids = ""
    for match in matches:
        ids = ids + match[1] + "%2C"
    ids = ids[:-3]

    url = "http://mymovieapi.com/?ids=" + ids + "&type=json&plot=simple&episode=1&lang=en-US&aka=simple&release=simple&business=0&tech=0"

    result = urlopen(url).read()
    try:
        movies = json.loads(result)
    except ValueError:
        return

    if ('error' in movies):
        return

    response = []
    for movie in movies:
        title = movie['title'].encode("utf-8")
        year =  " " + str(movie['year']) if "year" in movie else ""
        rating = "[" + str(movie['rating']) + "] " if "rating" in movie else ""
        plot =  "- " + movie['plot_simple'].encode("utf-8") if "plot_simple" in movie else ""
        countries = ""
        for country in movie['country']:
            countries = countries + country.encode("utf-8") + "/"
        countries = countries[:-1]
        response.append(title + " (" + countries + year + ") " + rating + plot)

    return response
