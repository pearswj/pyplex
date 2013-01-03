import requests
from requests import post
import xml.etree.ElementTree as ET

def loginMyPlex(user,password):
    url="https://my.plexapp.com/users/sign_in.xml"
    auth=(user,password)
    headers={"Content-Type":"application/xml",
        "X-Plex-Client-Identifier":"foobar",
        "X-Plex-Product": "Plex Media Center",
        "X-Plex-Version": "XXX",
        "X-Plex-Provides": "player",
        "X-Plex-Platform":"linux-rpi"}

    token = None
   
    try:
        response = requests.post(url,auth=auth,headers=headers)
        root = ET.fromstring(response.text)
        token = root.findall('authentication-token')[0].text
        user = root.findall('username')[0].text
        print "Logged in to myPlex as {:}".format(user)
    except:
        print "Could not login"
    return token


def listServers(token):
    url="https://my.plexapp.com/pms/servers.xml"
    payload = {"X-Plex-Token":token}
   
    response = requests.get(url,params=payload)
    print response.text

