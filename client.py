#!/usr/bin/env python2.7

#MineBot
#GPL and all that
# - espes


import urllib
import logging
from sys import argv
from getpass import getpass

from twisted.internet import reactor
from twisted.python import log

from BotProtocol import BotFactory
from Interface import CommandLineBotInterface, runReactorWithTerminal

from settings import *

#twisted idiom fail, yeah
def main():
    logging.basicConfig(filename="client.log", level=logging.CRITICAL)
    #observer = log.PythonLoggingObserver()
    #observer.start()
    
    
    loginname = argv[1]
    server = argv[2]
    port = int(argv[3])
    
    botname = None
    if len(argv) >= 5:
        botname = argv[4]
    
    if ENABLE_AUTH:
        password = getpass()
    
        logging.info("Logging in")
        params = urllib.urlencode({'user': loginname, 'password': password, 'version': 9001})
        handler = urllib.urlopen("http://login.minecraft.net/", params)
        ret = handler.read()
        logging.debug(ret)
        if ret == "Bad login1":
            logging.error(ret)
            return -1
    
        version, downloadTicket, username, sessionId= ret.split(":")

#        version = 22
#        downloadTicket = ""
#        username = "grotiiy"
#        sessionId = 1111
        logging.info("Got %r %r %r %r" % (version, downloadTicket, username, sessionId))
        
        if not botname: botname = username
    else:
        sessionId = 0
        if not botname: botname = loginname
        username = botname
    interfaceNamespace = {}
    
    f = BotFactory(username, sessionId, botname, interfaceNamespace)
    logging.info("tcptwisted")
    reactor.connectTCP(server, port, f)
    logging.info("tcptwisted")

   
    if ENABLE_CONSOLE:
        #start with a null oberserver to remove DefaultObserver
        #because we can't stderr in a terminal
        log.startLoggingWithObserver(lambda a: '')

        runReactorWithTerminal(CommandLineBotInterface, interfaceNamespace)
    else:
        reactor.run()

    
    

if __name__ == '__main__':
    main()
