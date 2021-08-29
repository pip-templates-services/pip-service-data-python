#!/usr/bin/env pwsh

# Pack archive for lambda
try {

    pip install -r requirements.txt --target ./package

    if (Test-Path "tmp") {
        Remove-Item -Recurse -Force -Path "tmp"
    }

    # Create tmp and copy dependency files and sources
    New-Item -ItemType Directory -Force -Path "tmp"
    New-Item -ItemType Directory -Force -Path "tmp/config"
    Copy-Item ./config/config.yml ./tmp/config/config.yml
    Copy-Item -Recurse ./package ./tmp/
    Copy-Item ./bin/lambda_function.py ./tmp/lambda_function.py

    # Create dist folder
    if (Test-Path "dist") {
        Remove-Item -Recurse -Force -Path "dist"
    }
    New-Item -ItemType Directory -Force -Path "dist"

    $component = Get-Content -Path "component.json" | ConvertFrom-Json

    $compress = @{
        Path             = "./tmp/*"
        CompressionLevel = "Optimal" #"NoCompression"
        DestinationPath  = "./dist/$($component.name)-lambda-v$($component.version).zip"
    }
    # Archiving
    Compress-Archive @compress

    Remove-Item -Recurse -Force -Path "tmp"

    Write-Host "The archive was successfully created."
}
finally {
    if (Test-Path "tmp") {
        Remove-Item -Recurse -Force -Path "tmp"
    }
}