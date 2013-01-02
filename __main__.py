import Queue
import traceback
import socket, subprocess, signal, os, logging
from pprint import pprint
import sys, platform

import listener.udplistener as udplistener
import listener.httplistener as httplistener
from zeroconf import ZeroconfService
from xbmc import xbmcCommands
from gui import BackgroundImage
  
def main():
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
    udp.setDaemon(True)
    udp.start()
    http = httplistener.httplistener(queue)
    http.setDaemon(True)
    http.start()
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    image = BackgroundImage('logo.png')
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

if __name__ == "__main__":
    hostname = platform.uname()[1]
    try:
        main()
    except Exception as e:
        print "Caught exception"
        #error(str(e))
        err = traceback.format_exc()
        print err


