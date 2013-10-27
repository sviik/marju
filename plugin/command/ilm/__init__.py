#!/opt/csw/bin/python
# coding=utf-8

from string import replace
from urllib import urlopen
import re

tartuIlmRe = re.compile('Temperatuur</A></TD><TD align="left" width="45%"><B>(?P<value>.*?) &deg;C</B>')

def getResponseType():
    return "MSG"

def getInfo():
    return "!ilm [asukoht] - väljastab asukoha temperatuuri. Parameetrita käsk annab asukohaloendi"

def get(parameter, folder):
    linn = parameter.title()
    if (linn == 'Tar' or linn == 'Tart' or linn == 'Tartu'):
        return get_tartu_ilm()
    if (linn == ''):
        return "Olemasolevad kohad: Dirhami, Heltermaa, Jõgeva, Jõhvi, Kihnu, Kunda, Kuusiku, Lääne-Nigula, Narva-Jõesuu, Pakri, Pärnu, Ristna, Rohuküla, Rohuneeme, Roomassaare, Ruhnu, Sõrve, Tallinn, Tartu, Tiirikoja, Türi, Valga, Viljandi, Vilsandi, Virtsu, Võru, Väike-Maarja"
    linn = replace(linn, '6', 'õ').decode("utf-8")
    linn = linn.encode("utf-8")
    linn = replace(linn, '2', 'ä').decode("utf-8")
    linn = linn.encode("utf-8")
    linn = replace(linn, 'y', 'ü').decode("utf-8")
    url = 'http://www.emhi.ee/index.php?ide=21&v_kaart=0'
    html = urlopen(url).read()
    regexp = '<td height="30">' + linn + '(?P<town>.*?)</td>' + "\n\t\t\t" + '<td align="center">(.*?)</td>' + "\n\t\t\t" + '<td align="center">(?P<value>.*?)</td>'
    match = re.search(regexp, html)
    if (match):
        linn = linn.encode("utf-8")
        temp = match.group("value")
        town = match.group("town")
        return linn + town + ": " + temp

def get_tartu_ilm():
    url = "http://meteo.physic.ut.ee/et/frontmain.php"
    html = urlopen(url).read()
    match = re.search(tartuIlmRe, html)
    if (match):
        temp = match.group("value")
        return "Tartu: " + temp