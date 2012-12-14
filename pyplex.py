# import urllib2, re, xml.etree.cElementTree as et
# from pyplex.pyomx.pyomxplayer import OMXPlayer
# # from pyomxplayer import OMXPlayer
# from urlparse import urlparse
# # import avahi, dbus, sys, platform
# from pprint import pprint
# import socket, subprocess, signal, os, logging
# from threading import Thread
# import Queue
# import udplistener
# import httplistener
# from pyplex.commands.xbmc import xbmcCommands
# from pyplex.interfaces.plexInterface import PlexInterface
from pyplex.pyplexclass import pyPlex

#this is kind of my idea...
if __name__ == "__main__":
    pyPlex.start()

exit()
urls = (
    '/xbmcCmds/xbmcHttp','xbmcCmdsXbmcHttp',
    '/(.*)', 'stop', 'hello'
)

class hello:        
    def GET(self, message):
        return 'Hello, World'

http = None
udp = None

if __name__ == "__main__":
    hostname = platform.uname()[1]
    try:
        print "starting, please wait..."
        global service
        global queue
        global parsed_path
        global media_key
        global duration
        duration = 0
        args = len(sys.argv)
        if args > 1: 
            if sys.argv[1] == "hdmi":
                omxCommand = '-o hdmi'
                print "Audo output over HDMI"
        else:
            omxCommand = ''
            print "Audio output over 3,5mm jack"
        xbmcCmmd = xbmcCommands(omxCommand)
        media_key = None
        parsed_path = None
        queue = Queue.Queue()
        service = ZeroconfService(name= hostname + " PyPlex", port=3000, text=["machineIdentifier=" + hostname,"version=2.0"])
        service.publish()
        udp = udplistener.udplistener(queue)
        udp.start()
        http = httplistener.httplistener(queue)
        http.start()
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        f = open(os.path.join(__location__, 'image/logo.png'));
        image = image(f)
#        image.set()
        while True:
            try:
                command, args = queue.get(True, 2)
                print "Got command: %s, args: %s" %(command, args)
                if not hasattr(xbmcCmmd, command):
                    print "Command %s not implemented yet" % command
                else:
                    func = getattr(xbmcCmmd, command)
                    func(*args)
                
                # service.unpublish()
            except Queue.Empty:
                pass
            if(xbmcCmmd.isRunning()):
                # print omx.position
                xbmcCmmd.updatePosition()
    except:
        print "Caught exception"
        if(xbmcCmmd):
            xbmcCmmd.Stop("")
        if(udp):
            udp.stop()
            udp.join()
        if(http):
            http.stop()
            http.join()
        raise

