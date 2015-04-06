#!/opt/csw/bin/python
# coding=utf-8

from urllib import urlopen, urlencode
from marjubot import NICK as BOT_NICK

def getCommands():
    return ['qs', 'õs', '6s']

def getInfo():
    return "[otsisõna] Väljastab ÕS päringu vastuse"

def getResponseType():
    return "MSG"

def get(parameter, channel, author, folder):
    if (not parameter):
        return None
    params = {'bot' : BOT_NICK, 'query' : parameter, 'chan' : channel, 'place' : parameter, 'nick' : author}
    url = "http://api.estchat.ee/qs.php?" + urlencode(params)
    return urlopen(url).read()