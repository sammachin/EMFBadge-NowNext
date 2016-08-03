### Author: Sam Machin 
### License: MIT
### Appname: On NOW!
### Description: Whats on Now

import wifi
import ugfx
import pyb
import time
import buttons
from http_client import *
import json
import math

def showevent(stage, event):
	start = event['start_date']
	end = event['end_date']
	speaker = event['speaker']
	text = event['title']
	ugfx.set_default_font(ugfx.FONT_MEDIUM)	
	ugfx.area(0,0,ugfx.width(),ugfx.height(),0x0000)
	ugfx.text(10,10,stage,ugfx.GREY)
	ugfx.text(10,35,"Start: "+start,ugfx.GREEN)
	ugfx.text(10,60,"End: "+end,ugfx.RED)
	ugfx.text(10,85,"Speaker: "+speaker,ugfx.BLUE)
	linelen = 25
	lines = int(math.ceil(len(text)/linelen))
	for l in range(0, lines):
		pixels = l*25+110
		start = l*linelen
		end = l*linelen+linelen
		if end>len(text):
			end = len(text)
		linetext = text[start:end]
		ugfx.text(10,pixels,linetext,0xFFFF)
	return
	
def mainscreen():
	ugfx.area(0,0,ugfx.width(),ugfx.height(),0x0000)
	ugfx.set_default_font(ugfx.FONT_MEDIUM_BOLD)	
	ugfx.text(30,30,"EMF Schedule Now & Next ",ugfx.GREY)
	ugfx.text(40,75,"Press [A] to get events ",ugfx.BLUE)
	return

def getdata():
	url = 'http://'+server+':9002/schedule'
	resp = get(url).text
	return json.loads(resp)
	

def nownext():
	ugfx.text(50,120,"Loading... ",ugfx.YELLOW)
	data = getdata()
	venue = list()
	for i in data.keys():
	    venue.append(i)
	venue = sorted(venue)
	print(venue)
	vpos = 0
	hpos = 0
	showevent(venue[vpos], data[venue[vpos]][hpos])
	while True:
		if buttons.is_triggered("JOY_RIGHT"):
			print(vpos)
			vpos += 1
			if vpos > len(venue)-1:
				vpos -= 1
			else:
				pass
			showevent(venue[vpos], data[venue[vpos]][hpos])
		if buttons.is_triggered("JOY_LEFT"):
			print(vpos)
			vpos -= 1
			if vpos < 0:
				vpos = 0
			else:
				pass
			showevent(venue[vpos], data[venue[vpos]][hpos])
		if buttons.is_triggered("JOY_DOWN"):
			print(hpos)
			hpos = 1
			showevent(venue[vpos], data[venue[vpos]][hpos])
		if buttons.is_triggered("JOY_UP"):
			print(hpos)
			hpos = 0
			showevent(venue[vpos], data[venue[vpos]][hpos])
		if buttons.is_triggered("BTN_A"):
			# Need to Implement fetching description by ID here
			pass
		if buttons.is_triggered("BTN_B"):
			mainscreen()
			return

#Check and Connect to WiFi
if wifi.is_connected():
	pass
else:
	wifi.connect()

#Init GFX and Buttons
ugfx.init()
buttons.init()

#Server Address
server = 'imaclocal.sammachin.com'


#Main Screen
mainscreen()
while True:
	if buttons.is_triggered('BTN_A'):
		nownext()
	if buttons.is_triggered('BTN_B'):
		mainscreen()
		
		
	
 
