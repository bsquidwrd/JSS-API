##
# This is used to clear the User and Location information
#
# You can run this by typing the following:
#       .\create_jss_users.ps1 -file .\users.csv
#
# The file does not need to be on your Desktop or called users.csv
# The users.csv file must have these headers:
#       username, full_name, email, phone_number, position
#
# If you have any issues, please submit an issue on this GitHub Repo and
# I can try to help you at the next chance I get.
#
# Set the URL, Username and Password where stated below.
# They currently have placeholders in there, just replace them with your information
#
# For this script, the user you enter must have the following permissions:
#   - Users
#       - Create
##

param (
    [string]$file = $(throw "-file is required.")
)

$disableSSL = $true
$jssCredentials = @{
    "host" = "https://jss.example.com:8443";
    "username" = "username";
    "password" = "password"
}

try {
    Import-Module VCP_Credentials
    $jssCredentials = Get-VCPCredentials -jssapi
    $credsLoaded = $true
} catch {
    $credsLoaded = $false
}

if($disableSSL) {
    #Disable validation of SSL Certificates
    [System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}
}
#JSS Credentials that have administrative permissions
# I have my own Credentials Module for easy code distribution
$apiUsername = $jssCredentials.username
$apiPassword = $jssCredentials.password
$jssURL = $jssCredentials.host

if($credsLoaded) {
    $apiAuthKey = $jssCredentials.authKey
} else {
    $apiLogin = $apiUsername + ":" + $apiPassword
    $apiAuthBytes = [System.Text.Encoding]::UTF8.GetBytes($apiLogin)
    $apiAuthKey = "Basic " + [System.Convert]::ToBase64String($apiAuthBytes)
}

#Specifies we are sending XML and authentication
$contentType = "application/xml"
$headers = @{}
$headers["Accept"] = "application/xml"
$headers["Authorization"] = "$($apiAuthKey)"
$userAgent = "Powershell Script for JAMF JSS API/Created By Brandon Usher"

if($credsLoaded) {
    $baseurl = $jssURL + "/users"
} else {
    $baseurl = $jssURL + "/JSSResource/users"
}

$users = Import-Csv $file

foreach ($user in $users) {
    try {
        $body = "
        <user>
            <name>" + $user.username + "</name>
            <full_name>" + $user.full_name + "</full_name>
            <email>" + $user.email + "</email>
            <phone_number>" + $user.phone_number + "</phone_number>
            <position>" + $user.position + "</position>
        </user>
        "
        $result = ([xml](Invoke-WebRequest -Uri $baseurl -Body $body -Headers $headers -UserAgent $userAgent -ContentType $contentType -Method Post).Content).user
        Write-Host "Created JSS user $($user.username): $($result.id)"
    } catch {
        Write-Host $_.Exception.Message
        Write-Host "Error: $($user.username)"
    }
}
