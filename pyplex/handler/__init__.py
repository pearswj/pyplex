import Queue
import traceback
import socket, subprocess, signal, os, logging
from pprint import pprint
import platform

import pyplex.listener.udplistener as udplistener
import pyplex.listener.httplistener as httplistener
from pyplex.zeroconf import ZeroconfService
from pyplex.xbmc import xbmcCommands
from pyplex.gui import BackgroundImage
  
def mainLoop(analog):
    print "starting, please wait..."
    hostname = platform.uname()[1]
    duration = 0
    if(analog):
        omxCommand = ''
        print "Audio output over 3,5mm jack"
    else:
        omxCommand = '-o hdmi'
        print "Audo output over HDMI"
    xbmcCmmd = xbmcCommands(omxCommand)
    media_key = None
    parsed_path = None
    queue = Queue.Queue()
    service = ZeroconfService(name= hostname + " PyPlex", port=3000, text=["machineIdentifier=" + hostname,"version=2.0"])
    service.publish()
    udp = udplistener.udplistener(queue)
    udp.setDaemon(True)
    udp.start()
    http = httplistener.httplistener(queue)
    http.setDaemon(True)
    http.start()
    image = BackgroundImage(os.path.join(os.path.dirname(os.path.dirname(__file__)),'images/logo.png'))
    #image.set()
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
           #error(err)
            
        if(xbmcCmmd.isRunning()):
            # print omx.position
            xbmcCmmd.updatePosition()

def runLoop(analog=False):
    try:
        mainLoop(analog)
    except Exception as e:
        print "Caught exception"
        #error(str(e))
        err = traceback.format_exc()
        print err


