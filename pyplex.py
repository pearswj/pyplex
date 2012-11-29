import urllib2, re, xml.etree.cElementTree as et
from pyomxplayer import OMXPlayer
from urlparse import urlparse
import avahi, dbus, sys, platform
from pprint import pprint
import socket, pygame.image, pygame.display, subprocess, signal, os, logging
from threading import Thread
import Queue
import udplistener
import httplistener
from plexInterface import PlexInterface

__all__ = ["ZeroconfService"]
class ZeroconfService:
    """A simple class to publish a network service with zeroconf using
    avahi.

    """

    def __init__(self, name, port, stype="_plexclient._tcp",
                 domain="", host="", text=""):
        self.name = name
        self.stype = stype
        self.domain = domain
        self.host = host
        self.port = port
        self.text = text

    def publish(self):
        bus = dbus.SystemBus()
        server = dbus.Interface(
                         bus.get_object(
                                 avahi.DBUS_NAME,
                                 avahi.DBUS_PATH_SERVER),
                        avahi.DBUS_INTERFACE_SERVER)

        g = dbus.Interface(
                    bus.get_object(avahi.DBUS_NAME,
                                   server.EntryGroupNew()),
                    avahi.DBUS_INTERFACE_ENTRY_GROUP)

        g.AddService(avahi.IF_UNSPEC, avahi.PROTO_UNSPEC,dbus.UInt32(0),
                     self.name, self.stype, self.domain, self.host,
                     dbus.UInt16(self.port), self.text)

        g.Commit()
        self.group = g
        print 'Service published'

    def unpublish(self):
        self.group.Reset()
        
urls = (
    '/xbmcCmds/xbmcHttp','xbmcCmdsXbmcHttp',
    '/(.*)', 'stop', 'hello'
)

class hello:        
    def GET(self, message):
        return 'Hello, World'

class xbmcCommands:
    def __init__(self, omxArgs):
        self.media = None
        self.plex = PlexInterface()
        self.omx = None
        self.omxArgs = omxArgs

    def PlayMedia(self, fullpath, tag, unknown1, unknown2, unknown3):
        global parsed_path
        global media_key
        global duration
        
        parsed_path = urlparse(fullpath)
        media_path = parsed_path.scheme + "://" + parsed_path.netloc + tag

        self.media = self.plex.getMedia(fullpath)
        
        #print 'mediapath', mediapath
        if(self.omx):
            self.Stop()
        transcodeURL = self.media.getTranscodeURL()
        print transcodeURL
        self.omx = OMXPlayer(transcodeURL, args=self.omxArgs, start_playback=True)

    def Pause(self, message):
        if(self.omx):
            self.omx.set_speed(1)
            self.omx.toggle_pause()

    def Play(self, message):
        if(self.omx):
            ret = self.omx.set_speed(1)
            if(ret == 0):
                self.omx.toggle_pause()

    def Stop(self, message=""):
        if(self.omx):
            self.omx.stop()
            self.omx = None

    def stopPyplex(self, message):
        self.Stop()
        global service
        pygame.quit()
        exit()

    def SkipNext(self, message = None):
        if(self.omx):
            self.omx.increase_speed()

    def SkipPrevious(self, message = None):
        if(self.omx):
            self.omx.decrease_speed()

    def StepForward(self, message = None):
        if(self.omx):
            self.omx.increase_speed()

    def StepBack(self, message = None):
        if(self.omx):
            self.omx.decrease_speed()

    def BigStepForward(self, message = None):
        if(self.omx):
            self.omx.jump_fwd_600()

    def BigStepBack(self, message = None):
        if(self.omx):
            self.omx.jump_rev_600()

    def getMilliseconds(self,s):
        hours, minutes, seconds = (["0", "0"] + ("%s" % s).split(":"))[-3:]
        hours = int(hours)
        minutes = int(minutes)
        seconds = float(seconds)
        miliseconds = int(3600000 * hours + 60000 * minutes + 1000 * seconds)
        return miliseconds

    def getPosMilli(self):
        return self.getMilliseconds(self.omx.position)
    
    def setPlayed(self):
        self.media.setPlayed()

    def isFinished(self):
        if(self.omx):
            finished = self.omx.finished
        else:
            finished = True
        return finished
    
    def isRunning(self):
        if(self.omx):
            return True
        return False

    def updatePosition(self):
        if self.isFinished():
            if (self.getPosMilli() > (self.media.duration * .95)):
                self.setPlayed()
            self.Stop()
        else:
            self.media.updatePosition(self.getPosMilli())
        
class image:
    def __init__(self, picture):
        # pygame.init()
        self.picture = pygame.image.load(picture)
        self.picture = pygame.transform.scale(self.picture,(1280,1024))

    def set(self):
        # pygame.mouse.set_visible(False)
        pygame.display.set_mode(self.picture.get_size())
        main_surface = pygame.display.get_surface()
        main_surface.blit(self.picture, (0, 0))
        pygame.display.update()


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

