#!/opt/csw/bin/python
# coding=utf-8

from marjubot import COMMAND_PLUGINS
import pluginloader

def getResponseType():
    return "NOTICE"

def getInfo():
    return "!addquote [tsitaat] - lisab tsitaadi"

def get(parameter, folder):
    help = []
    help.append("!seen [nick] - millal kasutaja viimati kanalis viibis")
    for i in COMMAND_PLUGINS.keys():
        help.append(pluginloader.load(COMMAND_PLUGINS[i]).getInfo())
    return help
