#!/opt/csw/bin/python
# coding=utf-8

from random import choice

def getCommands():
    return ["quote"]

def getInfo():
    return "[otsisõna] Väljastab suvalise tsitaadi, mis sisaldab otsisõna"

def getResponseType():
    return "MSG"

def get(parameter, channel, author, folder):
    file = open(folder + "/tsitaadid.txt")
    matches = []
    for line in file:
        if parameter.lower() in line.lower():
            matches.append(line)
    if (len(matches) > 0):
        file.close()
        return choice(matches).strip()
    file.close()
    return None