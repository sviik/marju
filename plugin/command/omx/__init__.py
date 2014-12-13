#!/opt/csw/bin/python
# coding=utf-8

import codecs
import urllib2
from urllib import urlencode

def getCommands():
    return ["omx"]

def getInfo():
    return "!omx [aktsia lühinimi] - väljastab OMX aktsia hetkehinna ja päevase tõusuprotsendi"

def getResponseType():
    return "MSG"

def get(parameter, channel, author, folder):
    if parameter is None or parameter is "":
        return

    params = {'pg': 'mainlist', 'market': 'XTAL', 'downloadcsv': '1', 'csvstyle': 'englishc'}
    usock = urllib2.urlopen("http://www.nasdaqomxbaltic.com/market/?" + urlencode(params))
    reader = codecs.getreader("utf-16")
    fh = reader(usock)

    stock = None
    ticker = parameter.upper()
    for row in fh:
        row = row.encode("utf-8").rstrip('\r\n').split("\t")
        if (row[0][:3] == ticker):
            stock = row
            break
    fh.close()
    usock.close()

    if (stock == None):
        return "Ei leidnud seda aktsiat"

    name = stock[1]
    lastPrice = stock[11]
    currency = stock[3]
    change = stock[12]

    colour = "3"
    if (change == "-%"):
        change = "0%"
        colour = "9"
    elif (change[0] == "-"):
        colour = "4"
    else:
       change = "+" + change

    return name + " " + lastPrice + " " + currency + ' ' + '' + colour + ' ' + change

