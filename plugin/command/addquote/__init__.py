#!/opt/csw/bin/python
# coding=utf-8

def getCommands():
    return ["addquote"]

def getResponseType():
    return "NOTICE"

def getInfo():
    return "!addquote [tsitaat] - lisab tsitaadi"

def get(parameter, channel, author, folder):
    with open(folder + "/tsitaadid.txt", "a") as f:
        f.write(parameter + "\n")
    return "Tsitaat lisatud!"
