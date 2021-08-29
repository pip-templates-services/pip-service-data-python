#!/usr/bin/env pwsh

if (Test-Path "dist") {
    try {
        aws --version
    }
    catch {
        Write-Output "To deploy your lambda you need to install and configure aws cli"
        exit 1
    }

    $component = Get-Content -Path "component.json" | ConvertFrom-Json
    $functionName = "$($component.name)-$($component.version.replace('.', '-'))-function"
    $createdFunctions = (aws lambda list-functions | ConvertFrom-Json).Functions

    Set-Location ./dist

    # Exist function flag
    $isExist = $false

    # Check for exist
    for ($i = 0; $i -lt $createdFunctions.Count; $i++) {
        if ($createdFunctions[$i].FunctionName -eq $functionName) {
            $isExist = $true
        }
    }

    # Update or create new lambda function
    if ($isExist) {
        aws lambda update-function-code --function-name $functionName --zip-file "fileb://$($component.name)-lambda-v$($component.version).zip"
    }
    else {
        Write-Output "Lambda function is does not exist."

        $accountId = aws sts get-caller-identity --query Account --output text
        $region = aws configure get region

        aws lambda create-function --runtime python3.9 --role "arn:aws:lambda:$($region):$($accountId):function:$($functionName)" --function-name $functionName --zip-file "fileb://$($component.name)-lambda-v$($component.version).zip"
    }

}
else {
    Write-Output "To deploy your lambda first pack application with pack_lambda.ps1"
}
