#!/opt/csw/bin/python
# coding=utf-8

from urllib import urlopen
from xml.dom.minidom import parseString

def getInfo():
    return "!rand [rand] - väljastab rannainfot. Parameetrita käsk annab loendi"

def getResponseType():
    return "MSG"

def get(parameter, folder):
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
