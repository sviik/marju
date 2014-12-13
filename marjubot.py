#!/opt/csw/bin/python
# coding=utf-8

from time import time
from ircbot import SingleServerIRCBot, Channel
from irclib import nm_to_n, is_channel, parse_channel_modes
from datetime import datetime
import re
import json
from urllib import urlopen
import random
import conf.config as config
import logging
import sys
import traceback
import threading
import pluginloader
from logger import Logger

NICK = config.NICK
PASSWORD = config.PASSWORD
SERVER = config.SERVER
PORT = config.PORT
OWNER_NICK = config.OWNER_NICK
OWNER_PASS=config.OWNER_PASS
COMMAND_PLUGINS = pluginloader.findAllCommandPlugins()
INTERCEPTOR_PLUGINS = pluginloader.findAllInterceptorPlugins()

class MarjuBot(SingleServerIRCBot):
    def __init__(self, channels, nickname, password, server, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port), password], nickname, nickname)
        self.channelsDict = channels
        self.password = password
        self.botNick = nickname
        self.channels = {}
        self.logger = Logger(self.channels)

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_privnotice(self, c, e):
        pass

    def on_welcome(self, c, e):
        c.privmsg("nickserv", "identify " + PASSWORD)
        for ch in self.channelsDict.keys():
            channel = Channel()
            channel.logging = self.channelsDict[ch]["logging"]
            channel.folder = "channels/" + self.channelsDict[ch]["folder"]
            channel.ai = self.channelsDict[ch]["ai"]
            channel.old = self.channelsDict[ch]["old"]
            channel.quoting = self.channelsDict[ch]["quoting"]
            channel.seen = self.channelsDict[ch]["seen"]
            self.channels[ch] = channel
            c.join(ch)

    def on_topic(self, c, e):
        self.logger.logTopic(e)

    def on_currenttopic(self, c, e):
        self.logger.logCurrentTopic(e)

    def on_topicinfo(self, c, e):
        self.logger.logTopicInfo(e)

    def on_privmsg(self, c, e):
         nick = nm_to_n(e.source())
         if (nick != OWNER_NICK):
             return
         command = e.arguments()[0].split(" ",1)
         if (len(command) == 1 or command[0] != OWNER_PASS):
             return
         cmd = command[1]
         c.send_raw(cmd)

    def on_pubnotice(self, c, e):
        self.logger.logPubNotice(e)

    def on_nick(self, c, e):
        before = nm_to_n(e.source())
        after = e.target()
        for channelName, channel in self.channels.items():
            if channel.has_user(before):
                self.logger.logNick(channelName, before, after)
                self.doSeen(before, channelName, False)
                self.doSeen(after, channelName, True)

    def on_join(self, c, e):
        nick = nm_to_n(e.source())
        channel = e.target()
        if (nick == c.get_nickname()):
            if (not channel in self.channels):
                newChannel = Channel()
                newChannel.logging = self.channelsDict[channel]["logging"]
                newChannel.folder = "channels/" + self.channelsDict[channel]["folder"]
                newChannel.ai = self.channelsDict[channel]["ai"]
                newChannel.old = self.channelsDict[channel]["old"]
                newChannel.quoting = self.channelsDict[channel]["quoting"]
                self.channels[channel] = newChannel
            self.channels[channel].add_user(nick)
            self.logger.logSelfJoin(e, channel)
            return
        self.channels[channel].add_user(nick)
        self.logger.logJoin(e)
        self.doSeen(nick, channel, True)

    def on_part(self, c, e):
        nick = nm_to_n(e.source())
        if (nick == c.get_nickname()):
            self.logger.logSelfPart(e)
            return
        self.logger.logPart(e)
        channel = e.target()
        self.doSeen(nick, channel, False)

    def on_action(self, c, e):
        self.logger.logAction(e)

    def on_quit(self, c, e):
        nick = nm_to_n(e.source())
        for channelName, channel in self.channels.items():
            if channel.has_user(nick):
                self.logger.logQuit(e, channelName)
                self.doSeen(nick, channelName, False)

    def on_kick(self, c, e):
        kickee = e.arguments()[0]
        if (kickee == c.get_nickname()):
            self.logger.logSelfKick(e)
            return
        self.logger.logKick(e)
        self.doSeen(kickee, e.target(), False)

    def on_mode(self, c, e):
        modes = parse_channel_modes(" ".join(e.arguments()))
        self.logger.logMode(e, modes)

    def on_pubmsg(self, c, e):
        self.logger.logPubMsg(e)
        if (self.parseAndDoCommand(e)):
            return
        self.doInterceptors(e)

    def parseAndDoCommand(self, e):
        command = e.arguments()[0].split(" ",1)
        parameter = ""
        if (len(command) > 1):
            parameter = command[1].rstrip('\n')
        command = command[0]
        if (len(command) > 1 and command[0] == "!"):
            self.doCommand(e, command[1:], parameter)
            return True
        return False

    def doCommand(self, e, cmd, parameter):
        author = nm_to_n(e.source())
        channel = e.target()
        msg = ""
        if cmd == "disconnect":
            pass
            #self.disconnect()
        elif cmd == "die":
            pass
            #self.die()
        elif cmd == "seen" and self.isCommandAllowedForChannel(cmd, channel):
            msg = self.getSeen(channel, parameter)
        elif cmd in COMMAND_PLUGINS and self.isCommandAllowedForChannel(cmd, channel):
             threading.Thread(target=self.commandWorker, args=(cmd, parameter, channel, author)).start()
             return
        self.sendResponse(msg, "MSG", channel, author)

    def isCommandAllowedForChannel(self, cmd, channel):
        if (cmd in ["quote", "addquote", "quotestat"] and not self.channels[channel].quoting):
            return False
        if (cmd == "seen" and not self.channels[channel].seen):
            return False
        return True

    def commandWorker(self, cmd, parameter, channel, author):
        plugin = pluginloader.load(COMMAND_PLUGINS[cmd])
        responseType = plugin.getResponseType()
        response = plugin.get(parameter, channel, author, self.channels[channel].folder)
        self.sendResponse(response, responseType, channel, author)

    def sendResponse(self, response, responseType, channel, author):
        if not response:
            return
        c = self.connection
        if (type(response) is not list):
            response = [response]
        for line in response:
            if (responseType == "NOTICE"):
                c.notice(author, line)
            elif (responseType == "MSG"):
                c.privmsg(channel, line)
                line = "<" + c.get_nickname() + "> " + line
                self.logger.log(channel, line)

    def doInterceptors(self, e):
        channel = e.target()
        if (not is_channel(channel)):
            return
        msg = e.arguments()[0].strip()
        author = nm_to_n(e.source())
        for interceptor in INTERCEPTOR_PLUGINS:
            if (self.isInterceptorAllowedForChannel(interceptor, channel)):
                threading.Thread(target=self.interceptorWorker, args=(interceptor, msg, channel, author)).start()

    def isInterceptorAllowedForChannel(self, interceptor, channel):
        if (interceptor == "old" and not self.channels[channel].old):
            return False
        if (interceptor == "ai" and not self.channels[channel].ai):
            return False
        return True

    def interceptorWorker(self, interceptor, msg, channel, author):
        plugin = pluginloader.load(INTERCEPTOR_PLUGINS[interceptor])
        responseType = plugin.getResponseType()
        response = plugin.get(msg, author, self.channels[channel].folder)
        self.sendResponse(response, responseType, channel, author)

    def doSeen(self, nick, channel, isJoin):
         unixTime = str(int(time()))
         folder = self.channels[channel].folder
         f = open(folder + "/seen.txt","r")
         lines = f.readlines()
         f.close()
         nickFound = False
         for index, line in enumerate(lines):
             if (line.split(":")[0] == nick):
                 newLine = ""
                 nickFound = True
                 if (isJoin):
                     newLine = nick + ":" + unixTime + ":"
                 else:
                     newLine = line.split(":")
                     newLine[2] = unixTime
                     newLine = ":".join(newLine)
                 lines[index] = newLine + "\n"
                 break
         f = open(folder + "/seen.txt","w")
         for line in lines:
             f.write(line)
         if (not nickFound):
             if (isJoin):
                 f.write(nick + ":" + unixTime + ":" + "\n")
             else:
                 f.write(nick + "::" + unixTime + "\n")
         f.close()

    def getSeen(self, channel, parameter):
        if (not self.channels[channel].seen):
            return
        folder = self.channels[channel].folder
        for chname, chobj in self.channels.items():
            if (channel == chname):
                if (chobj.has_user(parameter)):
                    return parameter + " on kanalis"
                break
        file = open(folder + "/seen.txt")
        result = ""
        for line in file:
            line = line.split(":")
            nick = line[0]
            if (nick.lower() == parameter.lower()):
                start = line[1].strip()
                end = line[2].strip()
                timeFormat = '%d/%m/%Y %H:%M:%S'
                if (start and end):
                    start = datetime.fromtimestamp(int(start)).strftime(timeFormat)
                    end = datetime.fromtimestamp(int(end)).strftime(timeFormat)
                    result = "Kasutaja " + nick + " oli viimati siin kanalis " + start + " kuni " + end
                elif (start):
                    start = datetime.fromtimestamp(int(start)).strftime(timeFormat)
                    result = "Kasutajat " + nick + " nähti viimati siin kanalis, kui ta joinis " + start
                elif (end):
                    end = datetime.fromtimestamp(int(end)).strftime(timeFormat)
                    result = "Kasutajat " + nick + " nähti viimati siin kanalis, kui ta lahkus " + end
                else:
                    result = "???"
                break
        if (result):
            return result
        return "Kasutajat " + parameter + " ei leitud."

def log_uncaught_exceptions(ex_cls, ex, tb):
    if (ex_cls == KeyboardInterrupt):
        return
    logging.critical('{0}: {1}'.format(ex_cls, ex))
    logging.critical(''.join(traceback.format_tb(tb)))

def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format = '%(asctime)s %(levelname)s %(message)s',
        filename='exceptions.log',
    )

    sys.excepthook = log_uncaught_exceptions

    channels = config.channels
    bot = MarjuBot(channels, NICK, PASSWORD, SERVER, PORT,)
    logging.debug(bot.start())

if __name__ == "__main__":
    main()
