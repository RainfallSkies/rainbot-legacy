"""
RainBot v1.52 (i think)
An example on how NOT to do an IRC bot
See the readme for more
"""

import requests
from twisted.words.protocols import irc
from twisted.internet import protocol, reactor

import sys
import os
import random
import time
import re

import youtube_dl
import wikipedia

debug = 0

NICK = 'RainBot'
if debug == 1:
    CHANNEL = '#bottesting'
else:
    CHANNEL = '#techtalk'
PASSWORD = ''
nickpass = 'bleh'

class RainBot(irc.IRCClient):

    pendingquotefile = file('pendingquotes.txt', 'a+')
    pendingquestionfile = file('pendingquestions.txt', 'a+')

    dontkick = ['ChanServ']

    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        self.regNickServ()
        time.sleep(10)
        self.join(CHANNEL)
        print "Signed on as {}.".format(self.nickname)

    def regNickServ(self):
        self.msg('NickServ', 'identify %s' % nickpass)

    def joined(self, channel):
        print "Joined %s." % channel
        if debug == 1:
            self.msg(channel, "Debug Mode")

    def privmsg(self, user, channel, msg):

        """
        This is called when the bot receives a message from a channel or PM.
        And this part of the code is very messy. I should rewrite this soon.
        """

        self.lineRate = 1

        print '<' + user.split('!')[0] + '> ' + msg

        if 'ayy lmao' in msg.lower():
            if random.randint(0, 25) == 12:
                self.msg(channel, "ayy lmao")
                self.logfile[channel].write('<' + NICK + '> ayy lmao\n')

        if msg.lower() == "hi rainbot":
            self.msg(channel, "Hi!")
            self.logfile[channel].write('<' + NICK + '> Hi!\n')

        if user.split('!')[0].lower() == 'muffin':
            if msg.lower() == "right rainbot":
                self.msg(channel, 'Yep')
            if msg.lower() == "right, rainbot":
                self.msg(channel, 'Yep')

        if msg.lower().startswith('$r quote add'):
            newmsg = msg.replace('$r quote add ', '')
            self.pendingquotefile.write(newmsg + '\n')
            print "Quote \"%s\" added to pending list." % newmsg
            self.msg(channel, "Quote added!")
            self.logfile[channel].write('<' + NICK + '> Quote added!\n')

        """Quote Stuff"""
        if msg.lower() == '$r quote':
            lines = open('quotes.txt').read().splitlines()
            myline = random.choice(lines)
            self.msg(channel, myline)
            self.logfile[channel].write('<' + NICK + '> %s\n' % myline)

        if msg.lower().startswith('$m math'):
            self.lineRate = 2
            newmsg = msg.replace('$m math ', '')
            if user.split('!')[0] == 'Muffin':
                self.msg(channel, str(eval(newmsg)))
            else:
                """msg.split('+', '-', '*', '**', '/', '%')"""
                self.msg(channel, 'Disabled Command')

        if msg.lower() == '$r inhale':
            self.msg(channel, "inhale my dong enragement child")
            self.logfile[channel].write('inhale my dong enragement child\n')

        if msg.lower().startswith('$r wiki'):
            newmsg = msg.lower().replace("$r wiki ", "")
            res = wikipedia.summary(newmsg, sentences=2).encode("utf-8")
            self.msg(channel, res)
            self.msg(channel, 'https://en.wikipedia.org/wiki/%s' % newmsg.replace(" ", "_"))

        if msg.lower() == '$r info':
            self.msg(channel, "RainBot")
            self.msg(channel, "Yet another IRC bot")
            self.msg(channel, "2015 RainfallSkies (mufn)")
            self.logfile[channel].write('<' + NICK + '> RainBot\n')
            self.logfile[channel].write('<' + NICK + '> Yet another IRC bot\n')
            self.logfile[channel].write('<' + NICK + '> 2015 RainfallSkies (mufn)\n')

        if msg.lower() == 'what is gak?':
            self.msg(channel, 'It\'s GAK GAK GAK')
            self.logfile[channel].write('<' + NICK + '> It\'s GAK GAK GAK\n')

        if msg.lower() == 'lol':
            if random.randint(0, 500) == 500:
                self.msg(channel, 'lol')
                self.logfile[channel].write('<' + NICK + '> lol')

        if msg.lower().startswith('https://youtube.com/watch?v='):
            newmsg = msg.replace('https://youtube.com/watch?v=', '')
            ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
            with ydl:
                result = ydl.extract_info(msg, download=False)
            if 'entries' in result:
                video = result['entries'][0]
            else:
                video = result
            m, s = divmod(video['duration'], 60)
            h, m = divmod(m, 60)
            dur = "%d:%02d:%02d" % (h, m, s)
            self.msg(channel, 'YouTube: \"%s\" - Views: %s - Duration: %s' % (video['title'].encode('utf-8'), str("{:,}".format(video['view_count'])), str(dur)))

        if msg.lower().startswith('https://www.youtube.com/watch?v='):
            newmsg = msg.replace('https://www.youtube.com/watch?v=', '')
            ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
            with ydl:
                result = ydl.extract_info(msg, download=False)
            if 'entries' in result:
                video = result['entries'][0]
            else:
                video = result
            m, s = divmod(video['duration'], 60)
            h, m = divmod(m, 60)
            dur = "%d:%02d:%02d" % (h, m, s)
            self.msg(channel, 'YouTube: \"%s\" - Views: %s - Duration: %s' % (video['title'].encode('utf-8'), str("{:,}".format(video['view_count'])), str(dur)))

        if msg.lower() == '$r thesevoicesinmyhead':
            voices = ['WHY ARE YOU CONCERNED ABOUT', 'WHAT ARE YOU CONCERNED ABOUT', 'ARE YOU NOT AMUSED', 'ARE', 'AND', 'VOICES', 'SO ARE THE', 'SO ARE', 'VOICES IN MY HEAD',\
            'SEND HELP', 'BACK', 'FRONT', 'NO', 'YES', 'MELODY', 'AREN\'T YOU ALONE', 'SAVE ME', 'COMET', 'MUFFIN', 'RAIN', 'ALONE',\
            'SO ALONE', 'HELLO', 'MUSIC', 'WOULD YOU', 'PLEASE', 'I CAN\'T FEEL', 'GO AWAY', 'IS IT WRONG', 'IF ONLY I COULD', 'GOODBYE']
            result = '%s %s %s %s %s' % (random.choice(voices), random.choice(voices), random.choice(voices), random.choice(voices), random.choice(voices))
            self.msg(channel, result)

        if msg.lower() == '$r help':
            self.msg(channel, 'Sending commands to %s. Keep in mind this list is not yet complete.' % user.split('!')[0])
            self.logfile[channel].write('Sending commands to %s. Keep in mind this list is not yet complete.\n' % user.split('!')[0])
            self.msg(user.split('!')[0], '$r quote - Displays a random quote from the database')
            self.msg(user.split('!')[0], '$r quote add - Adds a quote to the pending list')
            self.msg(user.split('!')[0], '$r question add <question> - Adds a question to shortly be added. It doesn\'t have to be exact words, as long as I know what you are trying to ask.')
            self.msg(user.split('!')[0], '$r wiki - Gets the first two sentences from a wikipedia article')
            self.msg(user.split('!')[0], '$r inhale - Asks the channel to inhale my dong')
            self.msg(user.split('!')[0], '$r info - Displays info')
            self.msg(user.split('!')[0], '$r log - Grabs logs on available channels')
            self.msg(user.split('!')[0], 'Saying ayy lmao will cause me to do the same.')
            self.msg(user.split('!')[0], 'I will post the title of a youtube link.')
            self.msg(user.split('!')[0], 'Ask me a question!')

        if msg.lower().startswith('$r question submit'):
            newmsg = msg.lower().replace('$r question submit', '')
            self.pendingquestions.write(newmsg)
            self.msg('Question submitted for review. Will be added shortly.')
            self.logfile[channel].write('<' + NICK + '> Question submitted for review.')

        """Question stuff"""
        if msg.lower().startswith(NICK.lower()):
            if 'favorite food' in msg.lower():
                self.msg(channel, 'Muffin :3')
            if 'favorite drink' in msg.lower():
                self.msg(channel, 'Chocolate Milk is the best!')
            if 'favorite show' in msg.lower():
                self.msg(channel, 'Depends, what\'s recent?')
            if 'favorite movie' in msg.lower():
                self.msg(channel, 'Dunno')
            if 'favorite color' in msg.lower():
                self.msg(channel, '...RAINBOWS!')
            if 'favorite user' in msg.lower():
                self.msg(channel, 'Melody. What\'d you think I was gonna say?')
            if 'favorite pony' in msg.lower():
                self.msg(channel, 'Rainbow Dash')
            if 'best pony' in msg.lower():
                self.msg(channel, 'Rainbow Dash')
            if 'how old are you' in msg.lower():
                self.msg(channel, 'I do not have a set age. Sorry!')
            if 'how are you' in msg.lower():
                self.msg(channel, 'I\'m great! How about you?')
            if 'nice to meet you' in msg.lower():
                self.msg(channel, 'Nice to meet you, too!')
            if 'who are you' in msg.lower():
                self.msg(channel, 'I am a novice IRC bot made in python. I promise I\'m very nice to people and I have a great personality. Too bad I can\'t engage in proper conversation.')
            if 'what were you coded' in msg.lower():
                self.msg(channel, 'I was made in python.')
            if 'what were you made' in msg.lower():
                self.msg(channel, 'I was made in python.')
            if 'what do you love' in msg.lower():
                self.msg(channel, 'I love Muffin! Too bad she\'s already with someone.')
            if 'who do you love' in msg.lower():
                self.msg(channel, 'I love Muffin! Too bad she\'s already with someone.')
            if 'your code' in msg.lower():
                self.msg(channel, 'My source is not public yet.')
            if 'your source' in msg.lower():
                self.msg(channel, 'My source is not public yet.')
            if 'why' in msg.lower():
                self.msg(channel, 'Uh... Someone came into my house to interview me... yeah...')
            if 'gender' in msg.lower():
                self.msg(channel, 'I identify as female.')
            if 'boy or girl' in msg.lower():
                self.msg(channel, 'I idenitfy as female.')
            if 'male or female' in msg.lower():
                self.msg(channel, 'I identify as female.')
            if 'why didn\'t you respond' in msg.lower():
                self.msg(channel, 'Though I love to talk, I only have a set amount of questions I\'m programmed to respond to. Give me more questions with \'$r question add\'')

        """Operator crap."""
        if user.split('!')[0] not in self.dontkick:
            if 'nigg' in msg.lower():
                self.kick(channel, user.split('!')[0], 'Racism')

            if 'fag' in msg.lower():
                self.kick(channel, user.split('!')[0], 'Homophobia')

            if 'tranny' in msg.lower():
                self.kick(channel, user.split('!')[0], 'Transphobia')

            if 'so gay' in msg.lower():
                self.kick(channel, user.split('!')[0], 'Homophobia')

            if 'that\'s gay' in msg.lower():
                self.kick(channel, user.split('!')[0], 'Homophobia')

            if 'thats gay' in msg.lower():
                self.kick(channel, user.split('!')[0], 'Homophobia')

            if 'you\'re gay' in msg.lower():
                self.kick(channel, user.split('!')[0], 'Homophobia')

            if 'youre gay' in msg.lower():
                self.kick(channel, user.split('!')[0], 'Homophobia')

            if 'your gay' in msg.lower():
                self.kick(channel, user.split('!')[0], 'Homophobia and bad grammar')

            if 'no homo' in msg.lower():
                self.kick(channel, user.split('!')[0], 'Homophobia')

            if 'dyke' in msg.lower():
                self.kick(channel, user.split('!')[0], 'Homophobia')


        if msg.lower() == '$m quit':
            if not user.split('!')[0].lower() == 'muffin':
                self.msg(channel, "Only Muffin can shut me down.")
                self.logfile[channel].write('<' + NICK + '> Only Muffin can shut me down.\n')
            else:
                self.msg(channel, "Bye!")
                self.logfile[channel].write('<' + NICK + '> Bye!\n')
                self.quit("Shutting down for maintenance")

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        user = user.split('!', 1)[0]
        self.logfile[channel].write("* %s %s\n" % (user, msg))

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        old_nick = prefix.split('!')[0]
        new_nick = params[0]
        self.logfile[channel].write("*%s is now known as %s\n" % (old_nick, new_nick))

    def userJoined(self, user, channel):
        self.logfile[channel].write('%s has joined %s\n' % (user, channel))
        print '%s has joined %s' % (user, channel)

    def userLeft(self, user, channel):
        self.logfile[channel].write('%s has left %s\n' % (user, channel))
        print '%s has left %s' % (user, channel)

    def userQuit(self, user, quitMessage):
        self.logfile[channel].write('%s has quit. Reason: %s\n' % (user, quitMessage))
        print '%s has quit. Reason: %s' % (user, quitMessage)

class RainBotFactory(protocol.ClientFactory):
    protocol = RainBot

    def __init__(self, channel, nickname=NICK):
        self.channel = channel
        self.nickname = nickname

    def clientConnectionLost(self, connector, reason):
        os.rename('logs/pm.txt', 'logs/pm_%s.txt' % time.strftime("%c"))
        os.rename('logs/techtalk.txt', 'logs/techtalk_%s.txt' % time.strftime("%c"))
        os.rename('logs/shiftosnext.txt', 'logs/shiftosnext_%s.txt' % time.strftime("%c"))
        os.rename('logs/jamesbondsfunhouse.txt', 'logs/jamesbondsfunhouse_%s.txt' % time.strftime("%c"))
        os.rename('logs/bottesting.txt', 'logs/bottesting_%s.txt' % time.strftime("%c"))
        print "Lost connection (%s)" % reason


    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % reason

if __name__ == "__main__":
    channel = CHANNEL
    if PASSWORD:
        channel += ' {}'.format(PASSWORD)
    reactor.connectTCP('irc.alphachat.net', 6667, RainBotFactory(channel))
    reactor.run()


"""   """
