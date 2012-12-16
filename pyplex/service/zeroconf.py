import avahi, dbus, sys, platform
from ..pyplexlogger.logger import pyPlexLogger
class ZeroconfService:
    """A simple class to publish a network service with zeroconf using
    avahi.
    """
    def __init__(self, name, port, stype="_plexclient._tcp", domain="", host="", text=""):
        self.name = name
        self.stype = stype
        self.domain = domain
        self.host = host
        self.port = port
        self.text = text
        self.l = pyPlexLogger('ZeroconfService').logger

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
        self.l.info('Published avahi Service')
        self.l.info('Name: %s' % self.name)
        self.l.info('Port: %s' % self.port)
        self.l.info('Domain: %s' % self.domain)
        self.l.info('Host: %s' % self.host)
        self.l.info('Text: %s' % self.text)

    def unpublish(self):
        self.group.Reset()