#!/usr/bin/python3
#
# from: https://linuxacademy.com/blog/linux-academy/creating-an-irc-bot-with-python3/
#

import hashlib
import socket
import urllib.request


# variables
server = "chat.freenode.net" 
channel = "#demok8sws" 
botnick = "pywpchksumbot"
adminname = "wkandek" 
exitcode = "bye " + botnick 


def get_hash(u):
  try:
    page = urllib.request.urlopen(u)
    s = page.read()
    return hashlib.sha224(s).hexdigest()
  except:
    return "Error in URL retrieval"


def joinchan(chan):
  """join channel"""
  ircsock.send(bytes("JOIN "+ chan +"\n", "UTF-8")) 
  ircmsg = ""
  while ircmsg.find("End of /NAMES list.") == -1: 
    ircmsg = ircsock.recv(2048).decode("UTF-8")
    ircmsg = ircmsg.strip('\n\r')
    print(ircmsg)


def ping():
  """respond to server Pings"""
  ircsock.send(bytes("PONG :pingis\n", "UTF-8"))


def sendmsg(msg, target=channel):
  """send messages to the target"""
  # With this we are sending a ‘PRIVMSG’ to the channel. The ":” lets the server separate the target and the message.
  ircsock.send(bytes("PRIVMSG "+ target +" :"+ msg +"\n", "UTF-8"))


def send_hash(m):
  joinchan(channel)
  sendmsg(m)


def abc():
  joinchan(channel)
  while 1:
    ircmsg = ircsock.recv(2048).decode("UTF-8")
    ircmsg = ircmsg.strip('\n\r')
    print(ircmsg)

    if ircmsg.find("PRIVMSG") != -1:
      # extract Nick and msg
      name = ircmsg.split('!',1)[0][1:]
      message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]
      # nick length has to be less than 17
      if len(name) < 17:
        if name.lower() == adminname.lower() and message.rstrip() == exitcode:
          sendmsg("oh...okay. :'(")
          ircsock.send(bytes("QUIT \n", "UTF-8"))
          return
    else:
      # Check if the information we received was a PING request. If so, we call the ping() function we defined earlier so we respond with a PONG.
      if ircmsg.find("PING :") != -1:
        ping()

# main
urls = ['https://en.wikipedia.org', 
        'https://el.wikipedia.org',
        'https://de.wikipedia.org']
msgstr = ""
for url in urls:
    urlhash = get_hash(url)
    msgstr = msgstr + url + ":" + urlhash + " "

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667)) 
ircsock.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick + " " + botnick + "\n", "UTF-8")) # user information
ircsock.send(bytes("NICK "+ botnick +"\n", "UTF-8")) # assign the nick to the bot

send_hash(msgstr)
ircsock.send(bytes("QUIT \n", "UTF-8"))

