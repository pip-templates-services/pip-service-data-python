#!/usr/bin/env pwsh

Set-StrictMode -Version latest
$ErrorActionPreference = "Stop"

# Get component data and set necessary variables
$component = Get-Content -Path "component.json" | ConvertFrom-Json

$protoImage="$($component.registry)/$($component.name):$($component.version)-$($component.build)-proto"
$container=$component.name
$directoryName=$component.name -replace '-','_'

# Remove old generate files
if (Test-Path "$($directoryName)/protos") {
    Remove-Item -Path "$($directoryName)/protos/*" -Force -Include *.py -Exclude __init__.py
}

# Build docker image
docker build --build-arg COMPONENT_NAME="$($directoryName)" -f docker/Dockerfile.proto -t $protoImage .

# Create and copy compiled files, then destroy
docker create --name $container $protoImage
docker cp "$($container):/app/$($directoryName)/protos" ./"$($directoryName)"/
docker rm $container
