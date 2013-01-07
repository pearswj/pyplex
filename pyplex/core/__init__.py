
import os,sys
import signal
from twisted.python import log
from twisted.web import server, resource
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

UDP_PORT = 9777
HTTP_PORT = 3000
ACCEPTED_URIS="/xbmcCmds/xbmcHttp"
PID_FILE="/var/run/pyplex.pid"
LOG_FILE="/var/log/pyplex.log"

class HTTPHandler(resource.Resource):

    isLeaf = True

    def parseQuery(self, query ):
        from urllib2 import unquote

        string = unquote(query).replace("command=","")
        front = string.index("(")
        end = string.rindex(")")
        command = string[:front]
        commandArgs = string[front+1:end].split(';')
        
        return (command,commandArgs)


    def render_GET(self, request): 
        from urlparse import urlparse

        parsed = urlparse( request.uri )

        if parsed.path in ACCEPTED_URIS:
            command,commandArgs = self.parseQuery( parsed.query )

            reactor.callLater(0, handleCommand, command=command, commandArgs=commandArgs)

        else:
            log.err("Unhandled URI" + parsed.path)
            return "received"


class UDPHandler(DatagramProtocol):

    def datagramReceived(self, data, (host, port)):
        index = data.rindex("\x02");
        command = data[index+1:-1]
        reactor.callLater(0, handleCommand, command=command, commandArgs=[u''])

def handleCommand(command, commandArgs=None):
    global XBMC_HANDLER
    print "Handling command {:}({:})".format(command,commandArgs)

    if not hasattr(XBMC_HANDLER, command):
        log.err("Command {:} not implemented yet".format(command))
    else:
        func = getattr(XBMC_HANDLER, command)
        func(*commandArgs)


def updatePosition():
    global XBMC_HANDLER
    XBMC_HANDLER.updatePosition()
    reactor.callLater(1,updatePosition)

def main(analog):
    import traceback
    import platform
    from pyplex.gui import BackgroundImage
    from pyplex.zeroconf import ZeroconfService
    from pyplex.xbmc import xbmcCommands
    global XBMC_HANDLER

    log.startLogging(open(LOG_FILE,"w"))

    try:
        pidfile = open(PID_FILE, "w")
        pidfile.write(str(os.getpid()))
        pidfile.flush()
        pidfile.close()
        hostname = platform.uname()[1]
        if(analog):
            omxCommand = ''
            print "Audio output over 3,5mm jack"
        else:
            omxCommand = '-o hdmi'
            print "Audio output over HDMI"
        XBMC_HANDLER =  xbmcCommands(omxCommand)



        service = ZeroconfService(name= hostname + " PyPlex", port=HTTP_PORT, text=["machineIdentifier=" + hostname,"version=2.0"])
        service.publish()
        image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'images/logo.png')
        print image_path
        #image = BackgroundImage()
        #image.set()
        site = server.Site(HTTPHandler())
        updatePosition()
        reactor.listenUDP(UDP_PORT, UDPHandler())
        reactor.listenTCP(HTTP_PORT, site)
        reactor.run()


    except Exception as e:
        err = traceback.format_exc()
        log.err(err)


def signal_handler(signal, frame):
    global XBMC_HANDLER

    print 'You pressed Ctrl+C!'

    if (XBMC_HANDLER != None):
        XBMC_HANDLER.Stop()
    reactor.stop()
    sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)


