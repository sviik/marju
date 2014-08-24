#!/opt/csw/bin/python
# coding=utf-8

from urllib import urlopen, urlencode
from xml.dom.minidom import parseString
from marjubot import NICK as BOT_NICK

def getInfo():
    return "!vesi [vesi] - väljastab rannainfot"

def getResponseType():
    return "MSG"

def get(parameter, channel, author, folder):
    if (not parameter):
        return
    params = {'bot' : BOT_NICK, 'nick' : author, 'chan' : channel, 'place' : parameter}
    url = "http://geoff.nohik.net/meowbeach.php?" + urlencode(params)
    return urlopen(url).read()

def get_old(parameter, channel, author, folder):
    return "Info olemas ainult rannahooajal"
    url = "http://www.g4s.ee/beaches2.php"
    xml = urlopen(url).read()
    dom = parseString(xml)
    markers = dom.getElementsByTagName('marker')

    if (parameter == ''):
        beaches = 'Olemasolevad rannad: '
        for marker in markers:
          beach = marker.getAttribute('town').lower().encode("utf-8")
          beaches = beaches + beach + ', '
        return beaches[:-2]

    param = parameter.lower().decode("utf-8")
    for marker in markers:
        beach = marker.getAttribute('town').lower()
        if(beach.startswith(param)):
            waterTemp = marker.getAttribute('watertemp').encode("utf-8")
            airTemp = marker.getAttribute('airtemp').encode("utf-8")
            pop = marker.getAttribute('pop').encode("utf-8")
            beach = marker.getAttribute('town').encode("utf-8")
            time = marker.getAttribute('time').encode("utf-8")
            return beach + " kell " + time + " - Vesi: " + waterTemp + " Õhk: " + airTemp + " Inimesi: "+ pop
