#!/opt/csw/bin/python
# coding=utf-8

import imp
import os

CommandPluginFolder = "./plugin/command"
InterceptorPluginFolder = "./plugin/interceptor"
MainModule = "__init__"

def findAllCommandPlugins():
    return findAllPlugins(CommandPluginFolder)

def findAllInterceptorPlugins():
    return findAllPlugins(InterceptorPluginFolder)

def findAllPlugins(folder):
    plugins = {}
    for i in os.listdir(folder):
        location = os.path.join(folder, i)
        if not os.path.isdir(location) or not MainModule + ".py" in os.listdir(location):
            continue
        info = imp.find_module(MainModule, [location])
        plugins[i] = {"name": i, "info": info}
    return plugins

def load(plugin):
    return imp.load_module(MainModule, *plugin["info"])
