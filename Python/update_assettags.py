##
# This script was created by Brandon Usher on 2015/05/18
# This script may be distributed any way seen fit, so long as it remains free
# If you paid money for this script, immediately ask for a refund
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
    jssCred.isLoaded()
    credentials_loaded = True
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

requestHeaders = {
    'Content-Type': 'application/xml',
    'Accept': 'application/xml',
}

try:
    reader = csv.DictReader(open(importFile), delimiter=',', quotechar='"')
except Exception as e:
    print(e)
    sys.exit(0)

apiEndpoint = jssURL + "JSSResource/mobiledevices"

# Simply loop through all the records in the CSV, minus the header
# since the reader sees the first line as the reference point
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
            <general>
                <asset_tag>%s</asset_tag>
            </general>
        </mobile_device>
        """ % (import_values['asset_tag'])
        deviceURL = '%s/serialnumber/%s' % (apiEndpoint, import_values['serial_number'])
        # This is where the request is sent to update the asset tag of the device
        request = requests.put(deviceURL, data=xmlData, headers=requestHeaders, verify=verifySSL, auth=(jssAPIUsername, jssAPIPassword))
        #request = requests.get(deviceURL, auth=(jssAPIUsername, jssAPIPassword), verify=False)

        if request.status_code == 201:
            successMsg = 'Updated device %s with asset tag %s' % (import_values['serial_number'], import_values['asset_tag'])
            print(successMsg)
        elif request.status_code == 404:
            raise Exception(
                'Device %s with asset tag %s was not found in the JSS' % (import_values['serial_number'], import_values['asset_tag'])
                )
        else:
            raise Exception(
                request.text
            )

    except Exception as e:
        error_reached = True
        print(e)

if error_reached:
    print('Error importing devices')
else:
    print('Finished importing devices')
