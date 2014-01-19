#!/opt/csw/bin/python
# coding=utf-8

import fileinput
import string
from datetime import datetime

def getInfo():
    return "!lastlink [N] - väljastab kuni N eelmist linki"

def getResponseType():
    return "MSG"

def get(parameter, channel, author, folder):
    N = 1
    if parameter:
        params = parameter.rstrip().split(" ")
        if (len(params) > 0):
            try:
                N = int(params[0])
            except ValueError:
                pass

    f = open(folder + "/links.txt","r")
    lines = f.readlines()
    f.close()

    count = min(N, len(lines))

    response = []
    for line in lines[-count:]:
        data = line.rstrip().split(" ")
        lastTime = datetime.fromtimestamp(int(data[5])).strftime("%d/%m/%Y %H:%M:%S")
        response.append(lastTime + " " + string.join(data[0:2], ""))
    return response
