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
        print(i)
        location = os.path.join(folder, i)
        if not os.path.isdir(location) or not MainModule + ".py" in os.listdir(location):
            continue
        info = imp.find_module(MainModule, [location])
        plugin = {"name": i, "info": info}
        commands = load(plugin).getCommands()
        for command in commands:
            plugins[command] = plugin
    return plugins

def load(plugin):
    return imp.load_module(MainModule, *plugin["info"])
