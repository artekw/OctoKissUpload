#!/usr/bin/env python

"""
OctoKissUpload - Upload Gcode to Octoprint
Based on: https://github.com/quillford/OctoUpload

Todo
1: SSL support
"""

version = "0.01"

import sys
import os
import base64
import socket
import urllib
import urllib2
import mimetools

hostIP = '192.168.88.14'
octoPort = '5000'
apiKey = '7CC15816FBE74599B7C17DD898C38CA4'
sendLoc = 'local' # or 'sdcard'
gcodeExt = 'gcode'
sslBool = 'no'
printBool = 'no'
selectBool = 'yes'

timeout = 15
socket.setdefaulttimeout(timeout)

def prepare_file(infile, gcodeExt=gcodeExt):
	#remove extension user may have used on the filename
	outputName = infile.split(".")[0]
	print outputName

	#remove . user may have used on extension
	if gcodeExt.find(".") != -1:
		gcodeExt = gcodeExt.split(".")[1]
		#print gcodeExt

	#add extension user specifies
	if gcodeExt == "g":
		outputName = outputName + "." + gcodeExt
	elif gcodeExt == "gco":
		outputName = outputName + "." + gcodeExt
	else:
		outputName = outputName + ".gcode"
	print "Ext: " + outputName
	send_file(outputName)

def send_file(filename,
				sslBool=sslBool, 
				sendLoc=sendLoc,
				printBool=printBool,
				selectBool=selectBool,
				apiKey=apiKey,
				hostIP=hostIP,
				octoPort=octoPort):
	#username = "spec"
	#password = "password"
	outputName = os.path.split(filename)[1]

	#allows for SSL if user specifies
	if sslBool == "yes":
		protocol = "https://"
	else:
		protocol = "http://"

	#sends the gcode to either sd or local
	if sendLoc == "sdcard":
		url = protocol + hostIP + ":" + octoPort + "/api/files/sdcard"
	else:
		url = protocol + hostIP + ":" + octoPort + "/api/files/local"

	#makes sure user submits a valid option for selecting
	if selectBool != ('yes' or 'no'):
		selectBool = 'no'
	print "Select: " + selectBool

	#makes sure user submits a valid option for printing
	if printBool != ('yes' or 'no'):
		printBool = 'no'
	print "Print: " + selectBool

	filebody = open(filename, 'rb').read()
	mimetype = 'application/octet-stream'
	boundary = mimetools.choose_boundary()
	content_type = 'multipart/form-data; boundary=%s' % boundary

	body = []
	body_boundary = '--' + boundary
	body = [  body_boundary,
			'Content-Disposition: form-data; name="file"; filename="%s"' % outputName,
			'Content-Type: %s' % mimetype,
			'',
			filebody,
			'--' + boundary,
			'Content-Disposition: form-data; name="select"',
			'',
			selectBool,
			'--' + boundary,
			'Content-Disposition: form-data; name="print"',
			'',
			printBool,
			]

	body.append('--' + boundary + '--')
	body.append('')
	body = '\r\n'.join(body)

	req = urllib2.Request(url)
	# Uncomment below two lines for basic auth support. (Used in cases where haproxy is in front of octoprint, with basic auth enabled).
	#base64string = base64.encodestring('%s:%s' % (username, password))
	#req.add_header("Authorization", "Basic %s" % base64string)
	req.add_header('User-agent', 'Cura AutoUploader Plugin')
	req.add_header('Content-type', content_type)
	req.add_header('Content-length', len(body))
	req.add_header('X-Api-Key', apiKey)
	req.add_data(body)

	print "Uploading..."
	print urllib2.urlopen(req).read()
	print "Done"


if __name__ == '__main__':
	if len(sys.argv) < 2:
		sys.exit('usage: OctoKissUpload.py <filename>')
	infilename = sys.argv[1]
	prepare_file(infilename)
    
