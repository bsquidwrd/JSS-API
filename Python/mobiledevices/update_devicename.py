##
# This is used to update device names to be the same as the username assigned to the device
#
# You can run this by typing the following:
#       python update_devicename.py
#
# If you have any issues, please submit an issue on this GitHub Repo and
# I can try to help you at the next chance I get.
#
# Set the URL, Username and Password where stated below.
# They currently have placeholders in there, just replace them with your information
#
# For this script, the user you enter must have the following permissions:
#   - Mobile Devices
#       - Read
#       - Write
##

import requests, sys, json

# Set this to False if you have any errors
verifySSL = False

# Set this so it only goes through one device for testing
debug = True
debug_username = 'brandonusher'

# Set JSS Variables here
# JSS URL must end with / like so:
# https://jss.example.com:8443/
jssURL = 'https://jss.example.com:8443/'
jssAPIUsername = 'username'
jssAPIPassword = 'password'

# I have my own JSS Module for easy code publishing
try:
    from vcpmodule import credentials as jssCred
    credentials_loaded = jssCred.isLoaded()
    creds = jssCred.getJSS()
    jssURL = creds.url
    jssAPIUsername = creds.username
    jssAPIPassword = creds.password
except:
    credentials_loaded = False

##                              ##
# DO NOT CHANGE ANY OF THE BELOW #
##                              ##

error_reached = False

jssAPIURL = jssURL + "JSSResource"

requestHeaders = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}

try:
    result = json.loads(requests.get('%s/mobiledevices' % jssAPIURL, headers=requestHeaders, verify=verifySSL, auth=(jssAPIUsername, jssAPIPassword)).text)
    mobile_devices = result['mobile_devices']
except Exception as e:
    print(e)
    sys.exit(0)

# Simply loop through all the records in the JSS
for device in mobile_devices:
    try:
        # Get the device ID then assemble the url to fetch the rest of the device record
        device_id = device['id']
        if debug is True and device['username'].lower() != debug_username.lower():
            continue

        # Device name is the same as the username field. Get it, assemble the push URL then push it
        device_name = device['username']
        deviceNameURL = '%s/mobiledevicecommands/command/DeviceName/%s/id/%s' % (jssAPIURL, device_name, device_id)
        # This is where the request is sent to update the name of the device
        request = requests.post(deviceNameURL, headers=requestHeaders, verify=verifySSL, auth=(jssAPIUsername, jssAPIPassword))

        if request.status_code == 201:
            successMsg = 'Updated device name to %s' % (device_name)
            print(successMsg)
        else:
            raise Exception(
                request.text
            )

    except Exception as e:
        error_reached = True
        print(e)

if error_reached:
    print('Error renaming devices')
else:
    print('Finished renaming devices')
