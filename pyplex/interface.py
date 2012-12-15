from commands.xbmc import xbmcCommands
from gui.image import image
import platform
from pprint import pprint
from listeners.udplistener import udplistener
from listeners.httplistener import httplistener
from pyomx.pyomxplayer import OMXPlayer
from service.zeroconf import ZeroconfService
import Queue
# from interfaces.plexInterface import plexInterface
# from interfaces.plexInterface
# from listners.httplistner import
class pyPlex():
	"""Wrapper class for pyPlex"""
	def __init__(self, arg):
		self.omxCommand = self.getArg(arg)
		self.hostname = platform.uname()[1]

	def start(self):
		"""Start listners and all other stuff"""
		# try:
		print "starting, please wait..."
		global service
		global queue
		global parsed_path
		global media_key
		global duration
		self.service = ZeroconfService(name=self.hostname + " PyPlex", port=3000, text=["machineIdentifier=" + self.hostname,"version=2.0"])
		self.service.publish()
		self.duration = 0
		self.xbmcCmmd = xbmcCommands(self.omxCommand)
		self.media_key = None
		self.parsed_path = None
		self.queue = Queue.Queue()
		self.udp = udplistener(self.queue)
		self.udp.start()
		self.http = httplistener(self.queue)
		self.http.start()
		# __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
		# f = open(os.path.join(__location__, 'image/logo.png'));
		# image = image(f)
		#image.set()
		# except:
		# 	print "error accoured"
		
	def run(self):
		"""Run pyPlex"""
		hostname = platform.uname()[1]
		try:
			# print "starting, please wait..."
			# global service
			# global queue
			# global parsed_path
			# global media_key
			# global duration
			# duration = 0
			# xbmcCmmd = xbmcCommands(self.omxCommand)
			# media_key = None
			# parsed_path = None
			# queue = Queue.Queue()
			# service = ZeroconfService(name= self.hostname + " PyPlex", port=3000, text=["machineIdentifier=" + hostname,"version=2.0"])
			# service.publish()
			# udp = udplistener.udplistener(queue)
			# udp.start()
			# http = httplistener.httplistener(queue)
			# http.start()
			# __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
			# f = open(os.path.join(__location__, 'image/logo.png'));
			# image = image(f)
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

	def getArg(self, arg):
		if len(arg) > 1: 
			if arg[1] == "hdmi":
				self.omxCommand = '-o hdmi'
				print "Audo output over HDMI"
		else:
			self.omxCommand = ''
			print "Audio output over 3,5mm jack"