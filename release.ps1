#!/usr/bin/env pwsh

Set-StrictMode -Version latest
$ErrorActionPreference = "Stop"

# Get component data
$component = Get-Content -Path "component.json" | ConvertFrom-Json
$package = Get-Content -Path "setup.py"

$versionLine = $package | Select-String -Pattern 'version=' -CaseSensitive -SimpleMatch
$packageVersion = $versionLine.Line.substring(2+$versionLine.Line.indexOf('='), 5)

if ($component.version -ne $packageVersion) {
    throw "Versions in component.json and package.json do not match"
}

# Install utility
pip install twine

# Automatically login to npmjs
if ($env:NPM_USER -ne $null -and $env:NPM_PASS -ne $null -and $env:NPM_EMAIL -ne $null) {
    if (npm whoami -ne $env:NPM_USER) {
        npm-cli-login
    }
}

# Check if version exist on npmjs
$npmjsPackageVersions = npm view $package.name versions

if ($npmjsPackageVersions -ne $null -and $npmjsPackageVersions.Contains($package.version)) {
    Write-Host "Package already exists on npmjs, publish skipped."
} else {
    # Publish to npm repository
    npm publish
}