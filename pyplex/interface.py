from commands.xbmc import xbmcCommands
from gui.image import image
import platform
from listeners.udplistener import udplistener
from listeners.httplistener import httplistener
from service.zeroconf import ZeroconfService
import Queue
from pprint import pprint
# from interfaces.plexInterface import plexInterface
# from interfaces.plexInterface
# from listners.httplistner import
class pyPlex():
	"""Wrapper class for pyPlex"""
	def __init__(self, arg):
		self.omxCommand = self.getArg(arg)
		self.hostname = platform.uname()[1]

	def start(self):
		"""Setting up listners and all other stuff"""
		# try:
		print "Setting up listeners, please wait..."
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
		print "Starting pyPlex..."
		try:
			while True:
				try:
					command, args = self.queue.get(True, 2)
					print "Got command: %s, args: %s" %(command, args)
					classes = [self.xbmcCmmd, self]
					for _class in classes:
						if not hasattr(_class, command):
							print "Command %s not implemented in %s" % command, _class.__class__.__name__
						else:
							func = getattr(_class, command)
							func(*args)
				except Queue.Empty:
					pass
				# func, args = self.parseCommand()
				# print "Function is: %s" % func
				# print "argument is: %s" % args
				
				if(self.xbmcCmmd.isRunning()):
					self.xbmcCmmd.updatePosition()
		except:
			print "Caught exception"
			if(self.xbmcCmmd):
				print '%s is de boosdoener!' % ('xbmc')
				self.xbmcCmmd.Stop("")
			if(udp):
				print '%s is de boosdoener!' % ('udp')
				self.udp.stop()
				self.udp.join()
			if(http):
				print '%s is de boosdoener!' % ('http')
				self.http.stop()
				self.http.join()
			raise

	def getArg(self, arg):
		if len(arg) > 1: 
			if arg[1] == "hdmi":
				self.omxCommand = '-o hdmi'
				print "Audo output over HDMI"
		else:
			self.omxCommand = ''
			print "Audio output over 3,5mm jack"

	# def parseCommand(self):
	# 	try:
	# 		command, args = self.queue.get(True, 2)
	# 		print "Got command: %s, args: %s" %(command, args)
	# 		classes = [self.xbmcCmmd, self]
	# 		for _class in classes:
	# 			if not hasattr(_class, command):
	# 				print "Command %s not implemented in %s" % command, _class.__class__.__name__
	# 			else:
	# 				func = getattr(_class, command)
	# 		return [func, args]
	# 	except Queue.Empty:
	# 		pass

	def stopPyplex(self):
		self.xbmcCmmd.stop("")
		self.udp.stop()
		self.http.stop()
		self.service.unpublish()
