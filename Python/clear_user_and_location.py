##
# This is used to clear the User and Location information
#
# You can run this by typing the following:
#       python clear_user_and_location.py ~/Desktop/devices.csv
#
# The file does not need to be on your Desktop or called devices.csv
# The devices.csv file must have one header:
#       serial_number
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

import requests, csv, sys

# Location of the import file
importFile = sys.argv[1]
# Set this to False if you run into any errors
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

jssAPIURL = jssURL + "JSSResource/"
apiEndpoint = jssAPIURL + "mobiledevices/serialnumber/"

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
for row in reader:
    import_values = {}
    try:
        # This will loop through every column and import the values into the
        # import_values variable where we can reference it much easier
        for col in row:
            value = row[col]
            import_values[col] = str(value)

        # Now once all the columns are imported into import_values we can use the API
        # to update the device records

        # Data to be sent to server
        xmlData = """<?xml version='1.0' encoding='utf-8'?>
        <mobile_device>
            <location>
                <username />
                <real_name />
                <email_address />
                <position />
                <phone />
                <department />
                <building />
                <room />
            </location>
        </mobile_device>
        """ % (import_values['serial_number'])
        deviceURL = '%s/serialnumber/%s' % (apiEndpoint, import_values['serial_number'])
        # This is where the request is sent
        request = requests.put(deviceURL, data=xmlData, headers=requestHeaders, verify=verifySSL, auth=(jssAPIUsername, jssAPIPassword))

        if request.status_code == 201:
            successMsg = 'Cleared device %s' % (import_values['serial_number'])
            print(successMsg)
        elif request.status_code == 404:
            raise Exception(
                'Device %s was not found in the JSS' % (import_values['serial_number'])
                )
        else:
            raise Exception(
                request.text
            )

    except Exception as e:
        error_reached = True
        print(e)

if error_reached:
    print('Error clearing User and Location for devices')
else:
    print('Finished clearing User and Location for devices')
