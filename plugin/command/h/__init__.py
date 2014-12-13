#!/opt/csw/bin/python
# coding=utf-8

import marjubot
import pluginloader

def getCommands():
    return ["h"]

def getResponseType():
    return "NOTICE"

def formatCommands(commands):
    result = ""
    for command in commands:
        result = result + "!" + command + " "
    return result

def getInfo():
    return "Kuvab selle nimekirja"

def get(parameter, channel, author, folder):
    help = []
    help.append("!seen [nick] Millal kasutaja viimati kanalis viibis")
    for i in marjubot.COMMAND_PLUGINS.keys():
        plugin = pluginloader.load(marjubot.COMMAND_PLUGINS[i])
        help.append(formatCommands(plugin.getCommands()) + plugin.getInfo())
    return help
