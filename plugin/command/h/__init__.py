#!/opt/csw/bin/python
# coding=utf-8

#from marjubot import COMMAND_PLUGINS
import marjubot
import pluginloader

def getCommands():
    return ["h"]

def getResponseType():
    return "NOTICE"

def getInfo():
    return "!h kuvab selle nimekirja"

def get(parameter, channel, author, folder):
    help = []
    help.append("!seen [nick] - millal kasutaja viimati kanalis viibis")
    for i in marjubot.COMMAND_PLUGINS.keys():
        help.append(pluginloader.load(marjubot.COMMAND_PLUGINS[i]).getInfo())
    return help
