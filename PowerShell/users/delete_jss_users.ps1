param (
    [string]$file = $(throw "-file is required."),
    [string]$output
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
    $baseurl = $jssURL + "JSSResource/users"
}

$users = Import-Csv $file

foreach ($user in $users) {
    try {
        $endUrl = $baseurl += "/name/" + $user.username
        $result = ([xml](Invoke-WebRequest -Uri $endUrl -Headers $headers -UserAgent $userAgent -ContentType $contentType -Method Delete).Content).user
        Write-Host "Deleted JSS user $($user.username): $($result.id)"
    } catch {
        Write-Host $_.Exception.Message
        Write-Host "Error: $($user.username)"
    }
}
