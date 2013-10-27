#!/opt/csw/bin/python
# coding=utf-8

def getResponseType():
    return "NOTICE"

def getInfo():
    return "!addquote [tsitaat] - lisab tsitaadi"

def get(parameter, folder):
    with open(folder + "/tsitaadid.txt", "a") as f:
        f.write(parameter + "\n")
    return "Tsitaat lisatud!"
