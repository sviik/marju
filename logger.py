#!/opt/csw/bin/python
# coding=utf-8

from time import strftime, localtime
from irclib import nm_to_n, nm_to_uh

class Logger():

    def __init__ (self, channels):
        self.channels = channels

    def log(self, channel, msg):
        if (not self.channels[channel].logging):
            return
        time = strftime("[%H:%M:%S] ", localtime())
        folder = self.channels[channel].folder
        with open(folder + "/log.txt", "a") as f:
            f.write(time + msg + "\n")

    def logWithoutTime(self, channel, msg):
        if (not self.channels[channel].logging):
            return
        folder = self.channels[channel].folder
        with open(folder + "/log.txt", "a") as f:
            f.write(msg + "\n")

    def logTopic(self, e):
        nick = nm_to_n(e.source())
        topic = e.arguments()[0]
        self.log(e.target(), "* " + nick + " changes topic to \'" + topic + "\'")

    def logCurrentTopic(self, e):
        topic = e.arguments()[1]
        channel = e.arguments()[0]
        self.log(channel, "* Topic is \'" + topic + "\'")

    def logTopicInfo(self, e):
        channel = e.arguments()[0]
        setter = e.arguments()[1]
        time = strftime("%a %b %d %H:%M:%S %Y", localtime(float(e.arguments()[2])))
        self.log(channel, "* Set by " + setter + " on " + time)

    def logPubMsg(self, e):
        nick = '<' + nm_to_n(e.source()) + '>'
        text =  ' ' + e.arguments()[0]
        log = nick + text
        self.log(e.target(), log)

    def logPubNotice(self, e):
        message = e.arguments()[0].strip()
        channel = e.target()
        nick = nm_to_n(e.source())
        message = '-' + nick + ':' + channel + '- ' + message
        self.log(channel, message)

    def logNick(self, channel, before, after):
        self.log(channel, '* ' + before + ' is now known as ' + after)

    def logSelfJoin(self, e, channel):
        time = strftime("%a %b %d %H:%M:%S %Y", localtime())
        self.logWithoutTime(e.target(), "\nSession Start: " + time)
        self.logWithoutTime(e.target(), "Session Ident: " + channel)
        self.log(e.target(), "* Now talking in " + channel)

    def logJoin(self, e):
        nick = nm_to_n(e.source())
        channel = e.target()
        userHost = nm_to_uh(e.source())
        self.log(channel, "* " + nick + " (" + userHost + ") has joined " + channel)

    def logSelfPart(self, e):
        time = strftime("%a %b %d %H:%M:%S %Y", localtime())
        self.logWithoutTime(e, "Session Close: " + time)

    def logSelfKick(self, e):
        kicker = nm_to_n(e.source())
        self.log(e.target(), "* You were kicked by " + kicker)
        time = strftime("%a %b %d %H:%M:%S %Y", localtime())
        self.logWithoutTime(e.target(), "Session Close: " + time)

    def logPart(self, e):
        channel = e.target()
        userHost = nm_to_uh(e.source())
        nick = nm_to_n(e.source())
        self.log(e.target(), "* " + nick + " (" + userHost + ") has left " + channel)

    def logAction(self, e):
        nick = "<" + nm_to_n(e.source()) + "> "
        msg = e.arguments()[0]
        self.log(e.target(), "* " + nick + msg)

    def logQuit(self, e, channel):
        nick = nm_to_n(e.source())
        userHost = nm_to_uh(e.source())
        self.log(channel, "* " + nick + " (" + userHost + ") Quit")

    def logKick(self, e):
        kicker = nm_to_n(e.source())
        kickee = e.arguments()[0]
        self.log(e.target(), "* " + kickee + " was kicked by " + kicker)

    def logMode(self, e, modes):
        nick = nm_to_n(e.source())
        for mode in modes:
            signedMode = mode[0] + mode[1]
            if mode[2] is None:
                mode[2] = ""
            else:
                mode[2] = " " + mode[2]
            self.log(e.target(), "* " + nick + " sets mode " + signedMode + mode[2])

