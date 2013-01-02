
import os
import json
import requests
from requests import post
import xml.etree.ElementTree as ET

AUTH_FILE = os.path.join(os.path.expanduser("~"),".myplex.json")

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

def storeAuthentication(user=None, password=None):
    authDict = { "username":user,"password":password }
    jsonData = json.dumps(authDict)

    try:
        authFile = open ( AUTH_FILE, "w")
        authFile.write(jsonData)
        authFile.flush()
        authFile.close()
        print "myPlex Authentication data written to "+AUTH_FILE
    except Exception as e:
        err = traceback.format_exc()
        print "Error saving authentication data.\n{:}".format(err)

def loadAuthentication():
    user = None
    password=None

    if os.path.isfile(AUTH_FILE):
        try:
            params = json.load(open(AUTH_FILE))
            user = params["username"]
            password = params["password"]
           
        except Exception as e:
            err = traceback.format_exc()
            print "Could not load myPlex info from {:}.\n{:}".format(AUTH_FILE, err)
   
    else:
        print "No myPlex file at "+AUTH_FILE
    return (user,password)


def listServers(token):
    url="https://my.plexapp.com/pms/servers.xml"
    payload = {"X-Plex-Token":token}
   
    response = requests.get(url,params=payload)
    print response.text

