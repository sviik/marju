#!/opt/csw/bin/python
# coding=utf-8

import imp
import os

PluginFolder = "./plugins"
MainModule = "__init__"

def findAll():
    plugins = {}
    for i in os.listdir(PluginFolder):
        location = os.path.join(PluginFolder, i)
        if not os.path.isdir(location) or not MainModule + ".py" in os.listdir(location):
            continue
        print("Loading plugin " + i)
        info = imp.find_module(MainModule, [location])
        plugins[i] = {"name": i, "info": info}
    return plugins

def load(plugin):
    return imp.load_module(MainModule, *plugin["info"])
