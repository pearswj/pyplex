import urllib2, re, xml.etree.cElementTree as et
from urllib import urlencode
from urlparse import urlparse
import uuid, hmac, hashlib, base64, time
from plexAPI.server import Server

from ..pyplexlogger.logger import pyPlexLogger
from pprint import pprint
class PlexMedia:
    def __init__(self, mediaurl, serverSceme):
        self.l = pyPlexLogger("PlexMedia").logger
        self.media_url = mediaurl
        server = serverSceme.split(':')
        self.server = Server(server[0], server[1])
        self.media = self.server.getMedia(mediaurl, self.server)


    def getTranscodeURL(self, extension='mkv', format='matroska', videoCodec='libx264', audioCodec=None, continuePlay=False, continueTime=None, videoWidth='1280', videoHeight='720', videoBitrate=None):
        if(videoWidth > self.media['width']):
            videoWidth = self.media['width']
        if(videoHeight > self.media['height']):
            videoHeight = self.media['height']
        self.session = uuid.uuid4()
        args = dict()
#        args["width"] = videoWidth
#        args["height"] = videoHeight
#        args["format"] = format
#        args["fakeContentLength"] = self.duration * 1000
#        args['key'] = self.mediaKey
#        args["session"] = "%s" % self.session.hex
#        args["videoBitrate"] = 12000
#        args['videoCodec'] = videoCodec
        args['offset'] = 0
        args['3g'] = 0
        args['subtitleSize'] = 125
        args['secondsPerSegment'] = 10
        args['ratingKey'] = self.mediaKey
        args['key'] = self.transcodeBaseURL + "/library/metadata/%s" % self.mediaKey
        args["identifier"] = "com.plexapp.plugins.library"
        args["quality"] = 7
        args["url"] = self.fileURL
#        if(audioCodec):
#            args["audioCodec"] = audioCodec
#        else:
#            args["audioCodec"] = self.audio_codec
        transcodeURL = self.server.transcodeURL
        transcodeURL += urlencode(args)
        atime = int(time.time())
        message = transcodeURL + "@%d" % atime
        sig = base64.b64encode(hmac.new(PlexInterface.transcode_private, msg=message, digestmod=hashlib.sha256).digest())
        plexAccess = dict()
        plexAccess['X-Plex-Access-Key'] = PlexInterface.transcode_public
        plexAccess['X-Plex-Access-Time'] = atime
        plexAccess['X-Plex-Access-Code'] = sig
        plexAccess['X-Plex-Client-Capabilities'] = 'protocols=http-live-streaming,http-mp4-streaming,http-mp4-video,http-mp4-video-720p,http-streaming-video,http-streaming-video-720p;videoDecoders=h264{profile:high&resolution:1080&level:41};audioDecoders=aac,mp3,ac3,dts'
        transcodeURL = self.transcodeBaseURL + transcodeURL + "&" + urlencode(plexAccess)
        return transcodeURL

    def setPlayed(self):
        try:
            f = urllib2.urlopen(self.playedURL)
        except urllib2.HTTPError:
            print "Failed to update plex that item was played: %s" % setPlayPos
            pass

    def updatePosition(self, posMilli):
        #TODO: make setPlayPos a function
        try:
            f = urllib2.urlopen((self.updateURL % (posMilli)))
        except urllib2.HTTPError:
            print "Failed to update plex play time, url: %s" % setPlayPos
            pass
        
        

class PlexInterface:
    transcode_private = base64.b64decode('k3U6GLkZOoNIoSgjDshPErvqMIFdE0xMTx8kgsrhnC0=')
    transcode_public = 'KQMIY6GATPC63AIMC4R2'

    def __init__(self):
        pass

    def getMedia(self, mediaurl, serverSceme):
        return PlexMedia(mediaurl, serverSceme)
