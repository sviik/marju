#!/opt/csw/bin/python
# coding=utf-8

from urllib import urlopen, urlencode
from marjubot import NICK as BOT_NICK

def getCommands():
    return ["ilm"]

def getResponseType():
    return "MSG"

def getInfo():
    return "[asukoht] Väljastab asukoha temperatuuri. Parameetrita käsk annab asukohaloendi"

def get(parameter, channel, author, folder):
    if not parameter:
        return "Olemasolevad kohad: Dirhami, Heltermaa, Jõgeva, Jõhvi, Kihnu, Kunda, Kuusiku, Lääne-Nigula, Narva-Jõesuu, Pakri, Pärnu, Ristna, Rohuküla, Rohuneeme, Roomassaare, Ruhnu, Sõrve, Tallinn, Tartu, Tiirikoja, Türi, Valga, Viljandi, Vilsandi, Virtsu, Võru, Väike-Maarja"
    params = {'bot': BOT_NICK, 'nick': author, 'chan': channel, 'place': parameter}
    url = "http://api.estchat.ee/meowtemp.php?" + urlencode(params)
    return urlopen(url).read()
