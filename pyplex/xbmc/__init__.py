#import Queue
#import pygame.image, pygame.display
#import socket, subprocess, signal, os, logging
#import urllib2, re, xml.etree.cElementTree as et
from urlparse import urlparse
from threading import Thread
from pyplex.omxplayer import OMXPlayer
from pyplex.plexapi.plexInterface import PlexInterface





class xbmcCommands:
    def __init__(self, omxArgs):
        self.media = None
        self.plex = PlexInterface()
        self.omx = None
        self.omxArgs = omxArgs
        self.volume = 60

    def PlayMedia(self, fullpath, tag, unknown1, unknown2, viewOffset):
        global parsed_path
        global media_key
        global duration

        
        parsed_path = urlparse(fullpath)
        media_path = parsed_path.scheme + "://" + parsed_path.netloc + tag

        self.media = self.plex.getMedia(media_path)
        
        #print 'mediapath', mediapath
        if(self.omx):
            self.Stop()
        #transcodeURL = self.media.getTranscodeURL()
        # transcodeURL not working otb in mplayer, fileURL fails for mkv
        #transcodeURL = self.media.fileURL
        # resorting to getting the path to the actual file (breaks myPlex support)
        transcodeURL = '"' + self.media.file + '"' # quoted to avoid white-space errors
        requestInfo = urlparse(transcodeURL)
        self.server = requestInfo.netloc
        print transcodeURL
        self.omx = OMXPlayer(transcodeURL, args=self.omxArgs, start_playback=True)

        self.omx.set_volume(self.volume)

        # resume from "viewOffset" (mplayer only)
        try:
            self.omx._process.send('seek %i 2\n' % int(int(viewOffset)/1000))
        except ValueError:
            pass

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
            #self.omx = None


    def SkipNext(self, message = None):
        if(self.omx):
            self.omx.increase_speed()

    def SkipPrevious(self, message = None):
        if(self.omx):
            self.omx.decrease_speed()

    def StepForward(self, message = None):
        if(self.omx):
            #self.omx.increase_speed()
            self.omx.jump_fwd_30()

    def StepBack(self, message = None):
        if(self.omx):
            #self.omx.decrease_speed()
            self.omx.jump_rev_30()

    def BigStepForward(self, message = None):
        if(self.omx):
            self.omx.jump_fwd_600()

    def BigStepBack(self, message = None):
        if(self.omx):
            self.omx.jump_rev_600()

    def setvolume(self, v):
        if(self.omx):
            self.omx.set_volume(v)
        self.volume = v

    def getMilliseconds(self,s):
        hours, minutes, seconds = (["0", "0"] + ("%s" % s).split(":"))[-3:]
        hours = int(hours)
        minutes = int(minutes)
        seconds = float(seconds)
        miliseconds = int(3600000 * hours + 60000 * minutes + 1000 * seconds)
        return miliseconds

    def getPosMilli(self):
        position = None
        if ( self.omx != None):
            position = self.getMilliseconds(self.omx.position)
        return position
    
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
            if (self.media != None and self.getPosMilli() > (self.media.duration * .95)):
                self.setPlayed()
            self.media = None
            self.omx = None
            #self.Stop()
        else:
            position = self.getPosMilli()
            if ( position != None ):
                self.media.updatePosition( position )
 
