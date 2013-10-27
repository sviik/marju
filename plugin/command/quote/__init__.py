#!/opt/csw/bin/python
# coding=utf-8

from random import choice

def getInfo():
    return "!quote [otsisõna] - väljastab suvalise otsisõna sisaldava tsitaadi"

def getResponseType():
    return "MSG"

def get(parameter, folder):
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