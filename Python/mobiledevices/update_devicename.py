##
# This is used to update device records with an asset tag based off of a CSV file
#
# You can run this by typing the following:
#       python update_assettags.py ~/Desktop/assets.csv
#
# The file does not need to be on your Desktop or called assets.csv
# The assets.csv file must have two headers:
#       serial_number and asset_tag
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

# Simply loop through all the records in the CSV, minus the header
# since the reader sees the first line as the reference point
for device in mobile_devices:
    try:
        # Get the device ID then assemble the url to fetch the rest of the device record
        device_id = device['id']
        deviceEndpoint = '%s/mobiledevices/id/%s' % (jssAPIURL, device_id)
        tmp_device = requests.get(deviceEndpoint, headers=requestHeaders, verify=verifySSL, auth=(jssAPIUsername, jssAPIPassword))

        # Load the device information as JSON for easy parsing
        mobile_device = json.loads(tmp_device.text)['mobile_device']

        # Device name is the same as the username field. Get it, assemble the push URL then push it
        device_name = mobile_device['location']['username']
        deviceNameURL = '%s/mobiledevicecommands/command/DeviceName/%s/id/%s' % (jssAPIURL, device_name, device_id)
        # This is where the request is sent to update the asset tag of the device
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
