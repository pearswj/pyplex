from pyplex.interface import pyPlex
import sys
from pprint import pprint


if __name__ == "__main__":
	args = sys.argv
	pprint(args)
	plex = pyPlex(args)
	plex.start()
	try:
		plex.run()
	except:
		"error while trying to start pyplex"