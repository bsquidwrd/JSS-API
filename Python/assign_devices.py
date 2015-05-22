##
#
##

import requests, csv, sys

# Location of the file that contains serial_number and asset_tag columns
importFile = sys.argv[1]
# Set this to False if you have any errors
verifySSL = False

# Set JSS Variables here
# I have my own JSS Module for easy code publishing
try:
    from jssmodule import credentials as jssCred
    credentials_loaded = jssCred.isLoaded()
except:
    credentials_loaded = False

if credentials_loaded:
    creds = jssCred.getJSS()
    jssURL = creds.url
    jssAPIUsername = creds.username
    jssAPIPassword = creds.password
else:
    # JSS URL must end with / like so:
    # https://jss.example.com:8443/
    jssURL = 'https://jss.example.com:8443/'
    jssAPIUsername = 'username'
    jssAPIPassword = 'password'

##                              ##
# DO NOT CHANGE ANY OF THE BELOW #
##                              ##

error_reached = False

jssAPIURL = jssURL + "JSSResource/"

requestHeaders = {
    'Content-Type': 'application/xml',
    'Accept': 'application/xml',
}

try:
    reader = csv.DictReader(open(importFile), delimiter=',', quotechar='"')
except Exception as e:
    print(e)
    sys.exit(0)

# Go through and set device information

if error_reached:
    print('Error importing devices')
else:
    print('Finished importing devices')
