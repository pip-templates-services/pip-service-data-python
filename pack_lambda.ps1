#!/usr/bin/env pwsh

try {

    Set-StrictMode -Version latest
    $ErrorActionPreference = "Stop"

    # Get component data and set necessary variables
    $component = Get-Content -Path "component.json" | ConvertFrom-Json
    $docsImage = "$($component.registry)/$($component.name):$($component.version)-$($component.build)-lambda"
    $container = $component.name

    # Delete old zip package
    if (Test-Path "dist") {
        Get-ChildItem -Path "dist" | Remove-Item -Recurse -Force -Include "*.zip"
    }
    else {
        New-Item -ItemType Directory -Force -Path "dist"
    }

    # Build docker image
    docker build --build-arg COMPONENT_NAME="$($component.name.replace('-', '_'))" -f docker/Dockerfile.lambda -t $docsImage .

    # Create and download dependencies, then destroy
    docker create --name $container $docsImage
    docker cp "$($container):/usr/src/app/package" ./tmp/
    docker rm $container

    # Create tmp and copy dependency files and sources
    New-Item -ItemType Directory -Force -Path "tmp"
    New-Item -ItemType Directory -Force -Path "tmp/config"
    Copy-Item ./config/config.yml ./tmp/config/config.yml
    Copy-Item ./bin/lambda_function.py ./tmp/lambda_function.py

    # Pack archive for lambda

    $compress = @{
        Path             = "./tmp/*"
        CompressionLevel = "Optimal" #"NoCompression"
        DestinationPath  = "./dist/$($component.name)-lambda-v$($component.version).zip"
    }
    # Archiving
    Compress-Archive @compress

    Write-Host "The archive was successfully created."
}
finally {
    Remove-Item -Recurse -Force -Path "tmp"
}