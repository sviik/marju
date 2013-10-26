#!/opt/csw/bin/python
# coding=utf-8

def getInfo():
    return "!quotestat [otsisõna] - väljastab otsisõna sisaldavate tsitaatide koguarvu"

def get(parameter, folder):
    if (not parameter):
        count = sum(1 for line in open(folder + '/tsitaadid.txt'))
        return "Kokku on " + str(count) + " tsitaati."
    count = 0
    file = open(folder + "/tsitaadid.txt")
    for line in file:
        if parameter.lower() in line.lower():
            count += 1
    return 'Sõna "' + parameter + '" kohta on ' + str(count) + " tsitaati."
