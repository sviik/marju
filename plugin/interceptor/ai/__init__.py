#!/opt/csw/bin/python
# coding=utf-8

import random
from marjubot import NICK

def do(msg, author, folder):
    #save random message to AI vocabulary
    if (random.random() < 0.1):
       saveVoc(msg, folder)

    response = []
    #answer if bot's nick is mentioned
    if (NICK.lower() in msg.lower()):
        if (random.random() < 0.6):
            response.append(getVoc(folder))
    return response

def getVoc(folder):
    file = open(folder + "/sonavara.txt")
    line = next(file)
    for num, aline in enumerate(file):
        if random.randrange(num + 2): continue
        line = aline
    file.close()
    return line

def saveVoc(msg, folder):
    with open(folder + "/sonavara.txt", "a") as f:
        f.write(msg + "\n")
