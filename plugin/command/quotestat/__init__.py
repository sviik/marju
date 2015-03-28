#!/opt/csw/bin/python
# coding=utf-8

def getCommands():
    return ["quotestat"]

def getInfo():
    return "[otsisõna] Väljastab otsisõna sisaldavate tsitaatide koguarvu"

def getResponseType():
    return "MSG"

def get(parameter, channel, author, folder):
    if (not parameter):
        with open(folder + "/tsitaadid.txt") as file:
            count = sum(1 for line in file)
        return "Kokku on " + str(count) + " tsitaati."
    count = 0
    with open(folder + "/tsitaadid.txt") as file:
        for line in file:
            if parameter.lower() in line.lower():
                count += 1
    return 'Sõna "' + parameter + '" kohta on ' + str(count) + " tsitaati."
