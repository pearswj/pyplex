#Pyplex

##Introduction

This is an implementation of an idea on the Plex forums - that the Raspberry Pi
could use a Plex client that had no interface, and was just designed to be 
operated using an iOS device or similar as a remote. Only the very barest bones
functionality is here, but I hope that it is reasonably easy to extend.

##Dependencies

Must be installed by you:
+ libsdl with framebuffer and alsa support
+ avahi with dbus, gtk, and python support
+ omxplayer

Installed by setup.py:
+ tornado
+ requests
+ pygame

##How to build

###Gentoo

See https://github.com/dalehamel/PlexOverlay for the pyplex ebuild. 

    echo 'PORTDIR_OVERLAY="/usr/local/portage"' >> /etc/portage/make.conf.
    mkdir -p /usr/local/portage
    cd /usr/local/portage
    git clone  https://github.com/dalehamel/PlexOverlay 
    ln -s PlexOverlay/*
    emerge -av pyplex --autounmask-write
    etc-update # merge strategy 3
    emerge -av pyplex #this may take quite a while...





###Raspbian

	sudo apt-get update && sudo apt-get upgrade
	sudo wget https://raw.github.com/Hexxeh/rpi-update/master/rpi-update
	sudo cp rpi-update /usr/local/bin/rpi-update
	sudo chmod +x /usr/local/bin/rpi-update 
	sudo rpi-update 192
	sudo reboot
	sudo vim config.txt > to set arm_freq to 1000
	sudo reboot
	sudo apt-get install avahi-daemon
	sudo apt-get install python-pip
	sudo pip install tornado
	sudo pip install pexpect
	sudo pip install requests
	sudo apt-get install python-avahi 
	
##How to use


### Install to system

    python setup.py install

This will install a script called pyplex to /usr/bin (or wherever your system puts it)

Or you can run the package without installing it by running scripts/pyplex

### Usage:

    usage: pyplex [-h] [--hdmi] [--user USER] [--password PASSWORD]

    A daemon to listen for UDP plex playback requests, and relay them to OMXPlayer

    optional arguments:
        -h, --help           show this help message and exit
        --hdmi               Send audio over HDMI instead of 3.5mm jack
        --user USER          myPlex username. Will be saved once provided or updated if already exists.
        --password PASSWORD  myPlex password. Will be saved once provided or updated if already exists.

        
### Setup myPlex


Give pyplex your myPlex username and password:

    pyplex --user you@youremail.com --password yoursecret


This will store your authentication data in ~/.myplex.json. This is just a flatfile, so limit who has access to viewing it!

### Launch the daemon

Launch with 

    pyplex [--hdmi]

Where [hdmi] is optional to make sure audio is going
over hdmi, leaving it out will devault to the 3,5mm jack output.

Then 'Raspberry Plex' should appear as a player you can choose in your Plex
client. Choose your media, and select this as the player to play it on. It should 
begin playing on your Raspberry Pi! 

To control playback you can use the remote tab on your iDevice or android device.
Currently the following commands are supported:
```
Play
Pause
Fastforward
Fastbackward
Stop
```

Support can be found on the [Plex forum][plexForum] 


[plexForum]: http://forums.plexapp.com/index.php/topic/35906-raspberry-pi
