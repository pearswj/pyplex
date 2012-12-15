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
from pyplex.interface import pyPlex
import sys
from pprint import pprint

#this is kind of my idea...
if __name__ == "__main__":
	args = sys.argv
	pprint(args)
	plex = pyPlex(args)
	plex.start()
	try:
		plex.run()
	except:
		"error while trying to start pyplex"

# exit()
# urls = (
#     '/xbmcCmds/xbmcHttp','xbmcCmdsXbmcHttp',
#     '/(.*)', 'stop', 'hello'
# )

# class hello:        
#     def GET(self, message):
#         return 'Hello, World'

# http = None
# udp = None

# if __name__ == "__main__":
    

