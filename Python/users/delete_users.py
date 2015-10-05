##
# This is used to delete Users in the JSS
#
# You can run this by typing the following:
#       python delete_users.py ~/Desktop/users.csv
#
# The file does not need to be on your Desktop or called users.csv
# The users.csv file must have these headers:
#       username
#
# If you have any issues, please submit an issue on this GitHub Repo and
# I can try to help you at the next chance I get.
#
# Set the URL, Username and Password where stated below.
# They currently have placeholders in there, just replace them with your information
#
# For this script, the user you enter must have the following permissions:
#   - Users
#       - Delete
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
apiEndpoint = jssAPIURL + "users"

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
        # to delete the user records

        # This is where the request is sent
        userURL = "%s/name/%s" % (apiEndpoint, import_values['username'])
        request = requests.delete(userURL, headers=requestHeaders, verify=verifySSL, auth=(jssAPIUsername, jssAPIPassword))
        if request.status_code == requests.codes.ok:
            print('Deleted user %s' % (import_values['username']))
        elif request.status_code == 404:
            raise Exception(
                'Could not delete user %s' %(import_values['username'])
                )
        else:
            raise Exception(
                request.text
            )

    except Exception as e:
        error_reached = True
        print(e)

if error_reached:
    print('Error deleting users')
else:
    print('Finished deleting users')
