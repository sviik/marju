#!/opt/csw/bin/python
# coding=utf-8

from random import choice
from time import time
from ircbot import SingleServerIRCBot, Channel
from irclib import nm_to_n, is_channel, parse_channel_modes
from datetime import datetime
import re
import json
import fileinput
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
PLUGINS = pluginloader.findAll()

youtubeUrlRe = re.compile('(youtube\.com/watch\?v=|youtube\.com/watch\?.*&v=|youtu.be/)(?P<id>[A-Za-z0-9_-]{11})')

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
        for ch in self.channelsDict.keys():
            channel = Channel()
            channel.logging = self.channelsDict[ch]["logging"]
            channel.folder = self.channelsDict[ch]["folder"]
            channel.ai = self.channelsDict[ch]["ai"]
            channel.old = self.channelsDict[ch]["old"]
            channel.quoting = self.channelsDict[ch]["quoting"]
            channel.seen = self.channelsDict[ch]["seen"]
            self.channels[ch] = channel
            c.join(ch)
        c.privmsg("nickserv", "identify " + PASSWORD)

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

    def on_pubmsg(self, c, e):
        command = e.arguments()[0].split(" ",1)
        parameter = ""
        if (len(command) > 1):
            parameter = command[1].rstrip('\n')
        command = command[0]
        self.logger.logPubMsg(e)
        if (len(command) > 1 and command[0] == "!"):
            self.doCommand(c, e, command[1:], parameter)
        else:
            self.doYoutube(c, e)
            self.doAI(c, e)
            self.doImdb(c, e)
            self.doOld(c, e)
        return

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
                newChannel.folder = self.channelsDict[channel]["folder"]
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

    def doAI(self, c, e):
        channel = e.target()
        if (not is_channel(channel) or is_channel(channel) and not self.channels[channel].ai):
            return

        #save random message to AI vocabulary
        msg = e.arguments()[0].strip()
        if (random.random() < 0.1):
           self.saveVoc(msg, channel)

        #answer if bot's nick is mentioned
        if (c.get_nickname().lower() in msg.lower()):
            if (random.random() < 0.6):
                out = self.getVoc(channel)
                c.privmsg(channel, out)
                msg = "<" + c.get_nickname() + "> " + msg

    def getVoc(self, channel):
        folder = self.channels[channel].folder
        file = open(folder + "/sonavara.txt")
        line = next(file)
        for num, aline in enumerate(file):
            if random.randrange(num + 2): continue
            line = aline
        return line

    def saveVoc(self, msg, channel):
        folder = self.channels[channel].folder
        with open(folder + "/sonavara.txt", "a") as f:
            f.write(msg + "\n")

    def doYoutube(self, c, e):
        channel = e.target()
        if (not is_channel(channel)):
            return
        msg = e.arguments()[0].strip()
        matches = re.findall(youtubeUrlRe, msg)
        if (not matches):
            return
        for match in matches:
            id = match[1]
            url = 'http://gdata.youtube.com/feeds/api/videos/' + id + '?v=2&alt=jsonc'
            result = urlopen(url).read()
            response = json.loads(result)
            if ('error' in response):
                continue
            title = response['data']['title'].encode("utf-8")
            c.privmsg(channel, title)
            self.logger.log(channel, "<" + c.get_nickname() + "> " + title)

    def doImdb(self, c, e):
        channel = e.target()
        if (not is_channel(channel)):
            return
        msg = e.arguments()[0].strip()

        imdbUrlRe = re.compile('(imdb\.com/title/(?P<id>tt[0-9]{7}))')
        matches = re.findall(imdbUrlRe, msg)
        matches = list(set(matches))
        if (not matches):
            return
        ids = ""

        for match in matches:
            ids = ids + match[1] + "%2C"
        ids = ids[:-3]

        url = "http://mymovieapi.com/?ids=" + ids + "&type=json&plot=simple&episode=1&lang=en-US&aka=simple&release=simple&business=0&tech=0"
        result = urlopen(url).read()
        movies = json.loads(result)

        if ('error' in movies):
            return

        for movie in movies:
            title = movie['title'].encode("utf-8")
            year =  str(movie['year'])
            rating = "[" + str(movie['rating']) + "] " if "rating" in movie else ""
            plot =  "- " + movie['plot_simple'].encode("utf-8") if "plot_simple" in movie else ""
            countries = ""
            for country in movie['country']:
                countries = countries + country.encode("utf-8") + "/"
            countries = countries[:-1]
            response = title + " (" + countries + " " + year + ") " + rating + plot
            c.privmsg(channel, response)
            self.logger.log(channel, "<" + c.get_nickname() + "> " + response)

    def doOld(self, c, e):
        channel = e.target()
        if (not is_channel(channel) or is_channel(channel) and not self.channels[channel].old ):
            return
        linkRe = re.compile('(http://www\.|https://www\.|http://|https://|www\.)(?P<link>\S+)')
        msg = e.arguments()[0].strip()
        links = re.findall(linkRe, msg)
        if (not links):
            return
        folder = self.channels[channel].folder
        for link in links:
            found = False
            for line in fileinput.input(folder + "/links.txt", inplace=1):
                data = line.rstrip().split(":")
                if (data[0] == link[1]):
                    found = True
                    count = int(data[1])
                    response = "old x" + str(count) + "!!!"
                    c.privmsg(channel, response)
                    self.logger.log(channel, "<" + c.get_nickname() + "> " + response)
                    print(data[0] + ":" + str((count + 1)))
                else:
                     print(line.rstrip())
            if (not found):
                with open(folder + "/links.txt", "a") as f:
                    f.write(link[1] + ":1\n")

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
                newLine = nick + ":" + unixTime + ":" + "\n"
                f.write(newLine)
            else:
                newLine = nick + "::" + unixTime + "\n"
                f.write(newLine)
        f.close()

    def getQuote(self, channel, parameter):
        folder = self.channels[channel].folder
        file = open(folder + "/tsitaadid.txt")
        matches = []
        for line in file:
            if parameter.lower() in line.lower():
                matches.append(line)
        if (len(matches) > 0):
            file.close()
            return choice(matches).strip()
        file.close()
        return None

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

    def addquote(self, channel, parameter):
        folder = self.channels[channel].folder
        with open(folder + "/tsitaadid.txt", "a") as f:
            f.write(parameter + "\n")

    def getQuotestat(self, channel, parameter):
        folder = self.channels[channel].folder
        if (not parameter):
            count = sum(1 for line in open(folder + '/tsitaadid.txt'))
            return "Kokku on " + str(count) + " tsitaati."
        count = 0
        file = open(folder + "/tsitaadid.txt")
        for line in file:
            if parameter.lower() in line.lower():
                count += 1
        return 'Sõna "' + parameter + '" kohta on ' + str(count) + " tsitaati."

    def getHelp(self, c, nick):
        help = """!quote [otsisõna] - väljastab suvalise otsisõna sisaldava tsitaadi
!addquote [tsitaat] - lisab tsitaadi
!quotestat [otsisõna] - väljastab otsisõna sisaldavate tsitaatide koguarvu
!seen [nick] - millal kasutaja viimati kanalis viibis
"""
        for i in PLUGINS.keys():
            help = help + pluginloader.load(PLUGINS[i]).getInfo() + "\n"
        help = help.split('\n')
        for line in help:
            c.notice(nick, line)

    def doCommand(self, c, e, cmd, parameter):
        nick = nm_to_n(e.source())
        channel = e.target()
        c = self.connection
        msg = ""
        if cmd == "disconnect":
            pass
            #self.disconnect()
        elif cmd == "die":
            pass
            #self.die()
        elif cmd == "quote":
            if (self.channels[channel].quoting):
                pass
                msg = self.getQuote(channel, parameter)
        elif cmd == "addquote":
            if (self.channels[channel].quoting):
                self.addquote(channel, parameter)
                c.notice(nick, "Tsitaat lisatud")
        elif cmd == "quotestat":
            if (self.channels[channel].quoting):
                pass
                msg = self.getQuotestat(channel, parameter)
        elif cmd == "seen":
            msg = self.getSeen(channel, parameter)
        elif cmd == "h":
            self.getHelp(c, nick)
        elif cmd in PLUGINS:
             threading.Thread(target=self.worker, args=(self.sendResponse, cmd, parameter, channel, c)).start()
             return

        self.sendResponse(msg, channel, c)

    def worker(self, callback, cmd, parameter, channel, c):
        msg = pluginloader.load(PLUGINS[cmd]).get(parameter, channel)
        callback(msg, channel, c)

    def sendResponse(self, msg, channel, c):
        if (msg and type(msg) is not list):
            c.privmsg(channel, msg)
            msg = "<" + c.get_nickname() + "> " + msg
            self.logger.log(channel, msg)
        elif (msg and type(msg) is list):
            for line in msg:
                c.privmsg(channel, line)
                line = "<" + c.get_nickname() + "> " + line
                self.logger.log(channel, line)

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
