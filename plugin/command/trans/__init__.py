#!/opt/csw/bin/python
# coding=utf-8

from microsofttranslator import Translator
import conf.config as config

def getCommands():
    return ["trans", "tr"]

def getInfo():
    return "[lähtekeele kood] [sihtkeele kood] [tekst] Tõlkefunktsioon"

def getResponseType():
    return "MSG"

def get(parameter, channel, author, folder):
    if not parameter:
        return None
    params = parameter.split(" ",2)
    client = Translator(config.AZURE_CLIENT_ID, config.AZURE_CLIENT_SECRET)
    try:
        return client.translate(params[2], params[1], from_lang=params[0]).encode("utf-8")
    except:
        return "Viga! Kasutamine: !trans lähtekeelekood sihtkeelekood tekst"