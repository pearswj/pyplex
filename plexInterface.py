import web, urllib2, re, xml.etree.cElementTree as et
from urllib import urlencode
from urlparse import urlparse
import uuid

class PlexMedia:
    def __init__(self, mediaurl):
        self.media_url = mediaurl
        
        f = urllib2.urlopen(mediaurl)
        rawXML = f.read()
        f.close()
        tree = et.fromstring(rawXML)

        #get video
        self.videoTag = tree.find('./Video')
        self.mediaTag = tree.find('./Video/Media')
        self.partTag = tree.find('./Video/Media/Part')
        self.mediaKey = self.videoTag.attrib['ratingKey']
        parsed_path = urlparse(mediaurl)
        self.fileURL = parsed_path.scheme + "://" + parsed_path.netloc + self.partTag.attrib['key']
        self.duration = int(self.partTag.attrib['duration'])

        self.media_type = "Video"
        self.video_codec = self.mediaTag.attrib['videoCodec']
        self.audio_codec = self.mediaTag.attrib['audioCodec']
        self.width = self.mediaTag.attrib['width']
        self.height = self.mediaTag.attrib['height']
        self.title = self.videoTag.attrib['title']
        self.continueTime= self.videoTag.attrib['viewOffset']
        self.duration = int(self.partTag.attrib['duration'])
        self.playedURL = parsed_path.scheme + "://" + parsed_path.netloc + "/:/scrobble?key=" + str(self.mediaKey) + "&identifier=com.plexapp.plugins.library"
        self.updateURL =  parsed_path.scheme + "://" + parsed_path.netloc + '/:/progress?key=' + str(self.mediaKey) + '&identifier=com.plexapp.plugins.library&time=%s&state=playing' 
        self.transcodeURL = parsed_path.scheme + "://" + parsed_path.netloc + '/video/:/transcode/generic.%s?'


    def getTranscodeURL(self, format='mkv', videoCodec='libx264', audioCodec=None, continuePlay=False, continueTime=None, videoWidth='1280', videoHeight='720', videoBitrate=None):
        if(videoWidth > self.width):
            videoWidth = self.width
        if(videoHeight > self.height):
            videoHeight = self.height
        self.session = uuid.uuid4()
        args = dict()
        args["width"] = videoWidth
        args["height"] = videoHeight
        args["format"] = format
        args["fakeContentLength"] = self.duration
        args['key'] = self.mediaKey
        args["session"] = "%s" % self.session.hex
        args["videoBitrate"] = 12000
        args['videoCodec'] = videoCodec
        args["identifier"] = "com.plexapp.plugins.library"
        args["quality"] = 11
        args["url"] = self.fileURL
        if(audioCodec):
            args["audioCodec"] = audioCodec
        else:
            args["audioCodec"] = self.audio_codec
        transcodeURL = self.transcodeURL % (format)
        transcodeURL += urlencode(args)
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

    def __init__(self):
        pass

    def getMedia(self, mediaurl):
        return PlexMedia(mediaurl)
