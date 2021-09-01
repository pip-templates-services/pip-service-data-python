#!/usr/bin/env pwsh

# Get component data and set necessary variables
$component = Get-Content -Path "component.json" | ConvertFrom-Json
$buildImage="$($component.registry)/$($component.name):$($component.version)-$($env:TRAVIS_BUILD_NUMBER)-build"
$testImage="$($component.registry)/$($component.name):$($component.version)-$($env:TRAVIS_BUILD_NUMBER)-test"
$rcImage="$($component.registry)/$($component.name):$($component.version)-$($env:TRAVIS_BUILD_NUMBER)-rc"

# Clean up build directories
if (Test-Path "dist") {
    Remove-Item -Recurse -Force -Path "dist"
}

# Remove docker images
docker rmi $buildImage --force
docker rmi $testImage --force
docker rmi $rcImage --force
docker image prune --force

# Remove existed containers
$exitedContainers = docker ps -a | Select-String -Pattern "Exit"
foreach($c in $exitedContainers) { docker rm $c.ToString().Split(" ")[0] }

# remove cash and temp files 
Get-ChildItem -Path "." -Include "cache" -Recurse | Remove-Item -Recurse -Force
Get-ChildItem -Path "." -Include "dist" -Recurse | Remove-Item -Recurse -Force 
Get-ChildItem -Path "." -Include "$($component.name.replace('-', '_')).egg-info" -Recurse | Remove-Item -Recurse -Force 
Get-ChildItem -Path "." -Include "$($component.name.replace('-', '_'))/*.pyc" -Recurse | Remove-Item -Force 
Get-ChildItem -Path "." -Include "$($component.name.replace('-', '_'))/**/*.pyc" -Recurse | Remove-Item -Force 
Get-ChildItem -Path "." -Include "$($component.name.replace('-', '_'))/__pycache__" -Recurse | Remove-Item -Force 
Get-ChildItem -Path "." -Include "test/__pycache__" -Recurse | Remove-Item -Recurse -Force 
Get-ChildItem -Path "." -Include "test/**/__pycache__" -Recurse | Remove-Item -Recurse -Force 
