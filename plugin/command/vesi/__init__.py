#!/opt/csw/bin/python
# coding=utf-8

from urllib import urlopen, urlencode
from marjubot import NICK as BOT_NICK

def getCommands():
    return ["vesi"]

def getInfo():
    return "!vesi [vesi] - väljastab rannainfot"

def getResponseType():
    return "MSG"

def get(parameter, channel, author, folder):
    if (not parameter):
        return
    params = {'bot': BOT_NICK, 'nick': author, 'chan': channel, 'place': parameter}
    url = "http://geoff.nohik.net/meowbeach.php?" + urlencode(params)
    return urlopen(url).read()
