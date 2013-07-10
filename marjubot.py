#!/opt/csw/bin/python
# coding=utf-8

from random import choice
from time import gmtime, strftime, localtime, time
from string import replace
from ircbot import SingleServerIRCBot, Channel
from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr, nm_to_uh, is_channel, parse_channel_modes
from datetime import datetime
from xml.dom.minidom import parseString
import re
import json
from urllib import urlopen
import random
import conf.config as config
import logging
import sys
import traceback

NICK = config.NICK
PASSWORD = config.PASSWORD
SERVER = config.SERVER
PORT = config.PORT
OWNER_NICK = config.OWNER_NICK
OWNER_PASS=config.OWNER_PASS
GOOGLE_KEY = config.GOOGLE_KEY
GOOGLE_CX = config.GOOGLE_CX
FML_KEY = config.FML_KEY

youtubeUrlRe = re.compile('(youtube\.com/watch\?v=|youtube\.com/watch\?.*&v=|youtu.be/)(?P<id>[A-Za-z0-9_-]{11})')
tartuIlmRe = re.compile('Temperatuur</A></TD><TD align="left" width="45%"><B>(?P<value>.*?) &deg;C</B>')

class MarjuBot(SingleServerIRCBot):
    def __init__(self, channels, nickname, password, server, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port), password], nickname, nickname)
        self.channelsDict = channels
        self.password = password
        self.botNick = nickname

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
            channel.quoting = self.channelsDict[ch]["quoting"]
            channel.seen = self.channelsDict[ch]["seen"]
            self.channels[ch] = channel
            c.join(ch)

        c.privmsg("nickserv", "identify " + PASSWORD)

    def on_topic(self, c, e):
        nick = nm_to_n(e.source())
        topic = e.arguments()[0]
        self.log(e.target(), "* " + nick + " changes topic to \'" + topic + "\'")

    def on_currenttopic(self, c, e):
        topic = e.arguments()[1]
        channel = e.arguments()[0]
        self.log(channel, "* Topic is \'" + topic + "\'")

    def on_topicinfo(self, c, e):
        channel = e.arguments()[0]
        setter = e.arguments()[1]
        time = strftime("%a %b %d %H:%M:%S %Y", localtime(float(e.arguments()[2])))
        self.log(channel, "* Set by " + setter + " on " + time)

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
        self.log_msg(c, e)
        if (len(command) > 1 and command[0] == "!"):
            self.do_command(c, e, command[1:], parameter)
        else:
            self.do_youtube(c, e)
            self.ai(c, e)
        return

    def do_youtube(self, c, e):
        channel = e.target()
        if (not is_channel(channel) or is_channel(channel) and not self.channels[channel].ai):
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
            self.log(channel, "<" + c.get_nickname() + "> " + title)

    def on_pubnotice(self, c, e):
        message = e.arguments()[0].strip()
        channel = e.target()
        nick = nm_to_n(e.source())
        message = '-' + nick + ':' + channel + '- ' + message
        self.log(channel, message)

    def ai(self, c, e):
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

    def on_nick(self, c, e):
        before = nm_to_n(e.source())
        after = e.target()
        for name, ch in self.channels.items():
            if ch.has_user(before):
                self.log(name, '* ' + before + ' is now known as ' + after)
                self.seen(before, name, False)
                self.seen(after, name, True)

    def on_join(self, c, e):
        nick = nm_to_n(e.source())
        channel = e.target()
        if (nick == c.get_nickname()):
            if (not channel in self.channels):
                newChannel = Channel()
                newChannel.logging = self.channelsDict[channel]["logging"]
                newChannel.folder = self.channelsDict[channel]["folder"]
                newChannel.ai = self.channelsDict[channel]["ai"]
                newChannel.quoting = self.channelsDict[channel]["quoting"]
                self.channels[channel] = newChannel
            self.channels[channel].add_user(nick)
            time = strftime("%a %b %d %H:%M:%S %Y", localtime())
            self.logWithoutTime(e.target(), "\nSession Start: " + time)
            self.logWithoutTime(e.target(), "Session Ident: " + channel)
            self.log(e.target(), "* Now talking in " + channel)
            return
        self.channels[channel].add_user(nick)
        userHost = nm_to_uh(e.source())
        self.log(channel, "* " + nick + " (" + userHost + ") has joined " + channel)
        self.seen(nick, channel, True)

    def seen(self, nick, channel, isJoin):
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

    def on_part(self, c, e):
        channel = e.target()
        userHost = nm_to_uh(e.source())
        nick = nm_to_n(e.source())
        if (nick == c.get_nickname()):
            time = strftime("%a %b %d %H:%M:%S %Y", localtime())
            self.logWithoutTime(e, "Session Close: " + time)
            return
        self.log(e.target(), "* " + nick + " (" + userHost + ") has left " + channel)
        self.seen(nick, channel, False)

    def on_action(self, c, e):
        nick = "<" + nm_to_n(e.source()) + "> "
        msg = e.arguments()[0]
        self.log(e.target(), "* " + nick + msg)

    def on_quit(self, c, e):
        nick = nm_to_n(e.source())
        userHost = nm_to_uh(e.source())
        for name, ch in self.channels.items():
            if ch.has_user(nick):
                self.log(name, "* " + nick + " (" + userHost + ") Quit")
                self.seen(nick, name, False)

    def on_kick(self, c, e):
        kicker = nm_to_n(e.source())
        kickee = e.arguments()[0]
        if (kickee == c.get_nickname()):
            self.log(e.target(), "* You were kicked by " + kicker)
            time = strftime("%a %b %d %H:%M:%S %Y", localtime())
            self.logWithoutTime(e.target(), "Session Close: " + time)
            return
        self.log(e.target(), "* " + kickee + " was kicked by " + kicker)
        self.seen(kickee, e.target(), False)

    def on_mode(self, c, e):
        modes = parse_channel_modes(" ".join(e.arguments()))
        nick = nm_to_n(e.source())
        for mode in modes:
            signedMode = mode[0] + mode[1]
            if mode[2] is None:
                mode[2] = ""
            else:
                mode[2] = " " + mode[2]
            self.log(e.target(), "* " + nick + " sets mode " + signedMode + mode[2])

    def log_msg(self, c, e):
        nick = '<' + nm_to_n(e.source()) + '>'
        text =  ' ' + e.arguments()[0]
        log = nick + text
        self.log(e.target(), log)

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

    def get_quote(self, channel, parameter):
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

    def get_seen(self, channel, parameter):
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

    def add_quote(self, channel, parameter):
        folder = self.channels[channel].folder
        with open(folder + "/tsitaadid.txt", "a") as f:
            f.write(parameter + "\n")


    def quote_stat(self, channel, parameter):
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

    def get_ilm(self, parameter):
        linn = parameter.title()
        if (linn == 'Tar' or linn == 'Tart' or linn == 'Tartu'):
            return self.get_tartu_ilm()
        if (linn == ''):
            return "Olemasolevad kohad: Dirhami, Heltermaa, Jõgeva, Jõhvi, Kihnu, Kunda, Kuusiku, Lääne-Nigula, Narva-Jõesuu, Pakri, Pärnu, Ristna, Rohuküla, Rohuneeme, Roomassaare, Ruhnu, Sõrve, Tallinn, Tartu, Tiirikoja, Türi, Valga, Viljandi, Vilsandi, Virtsu, Võru, Väike-Maarja"
        linn = replace(linn, '6', 'õ').decode("utf-8")
        linn = linn.encode("utf-8")
        linn = replace(linn, '2', 'ä').decode("utf-8")
        linn = linn.encode("utf-8")
        linn = replace(linn, 'y', 'ü').decode("utf-8")
        url = 'http://www.emhi.ee/index.php?ide=21&v_kaart=0'
        html = urlopen(url).read()
        regexp = '<td height="30">' + linn + '(?P<town>.*?)</td>' + "\n\t\t\t" + '<td align="center">(.*?)</td>' + "\n\t\t\t" + '<td align="center">(?P<value>.*?)</td>'
        match = re.search(regexp, html)
        if (match):
            linn = linn.encode("utf-8")
            temp = match.group("value")
            town = match.group("town")
            return linn + town + ": " + temp

    def get_tartu_ilm(self):
        url = "http://meteo.physic.ut.ee/et/frontmain.php"
        html = urlopen(url).read()
        match = re.search(tartuIlmRe, html)
        if (match):
            temp = match.group("value")
            return "Tartu: " + temp

    def get_omx(self, parameter):
        if parameter is None or parameter is "":
            return
        url = "http://www.nasdaqomxbaltic.com/market/?pg=mainlist&lang=et"
        stock = parameter.upper()
        html = urlopen(url).read()
        regexp = stock + '[1A][LRT]</td> \n\t\t\t\t\t\t\t\t<td>[TLNRIGV]{3}</td> \n\t\t\t\t<td>[EURLTV]{3}</td> \n\t\t\t\t<td>(?P<price>.*?)<\/td> \n\t\t\t\t\t\t\t\t<td>(.*?)</td> \n\t\t\t\t<td class="[negpos]{0,3}">(?P<change>.*?)</td>'
        match = re.search(regexp, html)
        if (not match):
            return "Ei leidnud seda aktsiat"
        lastPrice = match.group("price")
        change = match.group("change")
        number = '[0-9]'
        positive = '[+]'
        colour = '4'
        if (re.search(positive,change)):
            colour = '3'
        if ( not re.search(number,change)):
            change = ' 0%'
            colour = '9'
        return lastPrice + ' ' + '' + colour + change

    def get_fml(self):
        url = "http://api.fmylife.com/view/random/?key=" + FML_KEY + "&language=en"
        content = urlopen(url).read()
        dom = parseString(content)
        text = dom.getElementsByTagName('text')[0]
        value = text.firstChild.nodeValue.encode("utf-8")
        return value

    def get_imdb(self, parameter):
        title = parameter.replace(' ', '+')
        url = "http://www.imdbapi.com/" + "?t=" + title
        r = urlopen(url).read()
        response = json.loads(r)
        if (response['Response'] == "True"):
            title = response["Title"].encode("utf-8")
            id = response["imdbID"].encode("utf-8")
            year = response["Year"].encode("utf-8")
            rating = response["imdbRating"].encode("utf-8")
            return title + " (" + year + ") [" + rating + "] http://www.imdb.com/title/" + id + "/";
        else:
            return "Ei leidnud seda filmi"

    def get_google(self, parameter):
        url = 'https://www.googleapis.com/customsearch/v1'
        key = GOOGLE_KEY
        cx = GOOGLE_CX
        num = '&num=3'
        query = '&q=' + parameter.replace(' ', '+')
        url = url + key + cx + num + query
        r = urlopen(url).read()
        response = json.loads(r)
        if (response['searchInformation']['totalResults'] == '0'):
            return 'Ei leidnud midagi'
        items = response['items']
        result = []
        for item in items:
            result.append(item['link'])
        return result

    def get_rand(self, parameter):
        url = "http://www.g4s.ee/beaches2.php"
        xml = urlopen(url).read()
        dom = parseString(xml)
        markers = dom.getElementsByTagName('marker')

        if (parameter == ''):
            beaches = 'Olemasolevad rannad: '
            for marker in markers:
              beach = marker.getAttribute('town').lower().encode("utf-8")
              beaches = beaches + beach + ', '
            return beaches[:-2]

        param = parameter.lower().decode("utf-8")
        for marker in markers:
            beach = marker.getAttribute('town').lower()
            if(beach.startswith(param)):
                waterTemp = marker.getAttribute('watertemp').encode("utf-8")
                airTemp = marker.getAttribute('airtemp').encode("utf-8")
                pop = marker.getAttribute('pop').encode("utf-8")
                beach = marker.getAttribute('town').encode("utf-8")
                time = marker.getAttribute('time').encode("utf-8")
                return beach + " kell " + time + " - Vesi: " + waterTemp + " Õhk: " + airTemp + " Inimesi: "+ pop

    def send_help(self, c, nick):
        help = """!quote [otsisõna] - väljastab suvalise otsisõna sisaldava tsitaadi
!addquote [tsitaat] - lisab tsitaadi
!quotestat [otsisõna] - väljastab otsisäna sisaldavate tsitaatide koguarvu
!seen [nick] - millal kasutaja viimati kanalis viibis
!google [otsingufraas] - Google otsing
!ilm [asukoht] - väljastab asukoha temperatuuri. Parameetrita käsk annab asukohaloendi
!rand [rand] - väljastab rannainfot. Parameetrita käsk annab loendi
!omx [aktsia lühinimi] - väljastab OMX aktsia hetkehinna ja päevase tõusuprotsendi
!imdb [Filmi nimi] - Tagastab filmi nime, aasta, hinde ja IMDB lingi
!fml - Suvaline postitus saidilt fmylife.com"""
        help = help.split('\n')
        for line in help:
            c.notice(nick, line)

    def do_command(self, c, e, cmd, parameter):
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
                msg = self.get_quote(channel, parameter)
        elif cmd == "addquote":
            if (self.channels[channel].quoting):
                self.add_quote(channel, parameter)
                c.notice(nick, "Tsitaat lisatud")
        elif cmd == "quotestat":
            if (self.channels[channel].quoting):
                pass
                msg = self.quote_stat(channel, parameter)
        elif cmd == "ilm":
            msg = self.get_ilm(parameter)
        elif cmd == "omx":
            msg = self.get_omx(parameter)
        elif cmd == "fml":
            msg = self.get_fml()
        elif cmd == "rand":
            msg = self.get_rand(parameter)
        elif cmd == "imdb":
            msg = self.get_imdb(parameter)
        elif cmd == "seen":
            msg = self.get_seen(channel, parameter)
        elif cmd == "google":
            msg = self.get_google(parameter)
        elif cmd == "h":
            self.send_help(c, nick)
        if (msg and type(msg) is not list):
            c.privmsg(channel, msg)
            msg = "<" + c.get_nickname() + "> " + msg
            self.log(channel, msg)
        elif (msg and type(msg) is list):
            for line in msg:
                c.privmsg(channel, line)
                line = "<" + c.get_nickname() + "> " + line
                self.log(channel, line)

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
