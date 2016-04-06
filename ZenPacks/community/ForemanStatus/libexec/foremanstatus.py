#!/usr/bin/python

import json 
import urllib2
import sys
import contextlib

if len(sys.argv) < 3:
    print 'Usage:'
    print sys.argv[0] + ' <foreman hostname> <machine name>'
    sys.exit(1)

foreman = sys.argv[1]
host = sys.argv[2]

request = ('https://' + foreman + '/api/hosts/' + host)
with contextlib.closing(urllib2.urlopen(request)) as response:
    data = response.read()

parsed = json.loads(data)

result = ""
returncode = 0

if parsed.get('global_status_label') is not None:
    globalstatus = parsed['global_status_label']

    if globalstatus == "Error":
        globalstatus = "Critical"
        returncode = 2

    if globalstatus == "Warning":
        returncode = 1
  
    result += globalstatus + ' Foreman Status: '
else:
    print "Foreman Error:"
    sys.exit(3)
 
if parsed.get('configuration_status_label') is not None:
    confstatus = parsed['configuration_status_label'] 
    result += 'Config ' + confstatus + ','


if parsed.get('build_status_label') is not None:
    buildstatus = parsed['build_status_label']
    result += ' Build ' + buildstatus

print result
sys.exit(returncode)

