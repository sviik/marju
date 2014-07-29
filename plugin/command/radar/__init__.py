#!/opt/csw/bin/python
# coding=utf-8

def getResponseType():
    return "MSG"

def getInfo():
    return "!radar Sürgavere radar"

def get(parameter, channel, author, folder):
    return "http://www.ilmateenistus.ee/ilm/ilmavaatlused/radaripildid/surgavere-radar/"
