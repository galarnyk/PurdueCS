#!/usr/bin/env python
import sys
import os
import re
import time
from subprocess import check_output as Sensor

from twython import Twython
CONSUMER_KEY = 'OUkS20RseKGJibhj3MehEQ'
CONSUMER_SECRET = '2FJSpis6FxaXIul4VKQ60UTvLTrXigil70oAtIKmk'
ACCESS_KEY = '2202399570-xQfFFGYxGP1Jt81z9DfEr8H2nJGGCKmC0HMlATE' 
ACCESS_SECRET = 'MDR8OQ5WAz1eVGB6Qs73EnNimwQX8qokLzVRCdABoa7v1'

api = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)

f=  open('/home/pi/raspicam/lastId.txt', 'r+')
lastid = int(f.read())

print lastid


mentions = api.get_mentions_timeline()

ids=[]
users=[]
text=[]

for m in mentions:
  ids.append(m["id"])
  users.append(m["user"]["screen_name"])
  text.append(m["text"])

for i in ids: 
  print i

for u in users:
  print u

for t in text:
  print t
f.seek(0)
f.write(str(ids[0])+ "\n")

#take a picture when run to store it in advance
cmd='raspistill -n -o /home/pi/raspicam/currimage.jpg'
os.system(cmd)

out = Sensor(["/home/pi/raspicam/digitemp-3.6.0/digitemp_DS9097U", "-s /dev/ttyUSB0 -a"])

currlight = out[149:151] #light
currtemp = out[140:144] #temp


for i, id in enumerate(ids):
  print lastid, id
  if id > lastid:
    if len(re.findall('pic',text[i])) > 1:
      print "wants picture"
      photo = open('/home/pi/raspicam/currimage.jpg', 'rb')
      reply = "@" + users[i] +" here you go!"
      print reply
      api.update_status_with_media(media=photo, status=reply)
    elif re.search('light', text[i]):
      print "wants light status"
      reply = "@" + users[i] + " the current light level is " + currlight
      print reply
      api.update_status(status=reply)
    elif re.search('temp', text[i]):
      print "wants temp status"
      reply = "@" + users[i] + " here is the current room temp: " + currtemp
      print reply
      api.update_status(status=reply)
    else:
      print "not a valid message send default response"
      reply = "@" + users[i] + " hello there!"
      print reply
      api.update_status(status=reply)
  else:
    print "not a new message"


f.close()
