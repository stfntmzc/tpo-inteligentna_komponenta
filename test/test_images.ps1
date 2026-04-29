# test_images.ps1

param(
    [string]$ApiUrl = "http://127.0.0.1:12000/api/moderate",
    [string]$ImageDir = "test/images"
)

Write-Host "Testing images from: $ImageDir"
Write-Host "API endpoint: $ApiUrl"
Write-Host "============================================================"

if (-Not (Test-Path $ImageDir -PathType Container)) {
    Write-Host "Error: image directory does not exist: $ImageDir"
    exit 1
}

$images = Get-ChildItem -Path $ImageDir -File

foreach ($image in $images) {
    Write-Host ""
    Write-Host "Image: $($image.FullName)"

    try {
        $response = Invoke-WebRequest `
            -Uri $ApiUrl `
            -Method Post `
            -Form @{
                file = Get-Item $image.FullName
            }

        Write-Host "HTTP status: $($response.StatusCode)"
        Write-Host "Response:"

        $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 20

    } catch {
        Write-Host "Request failed."

        if ($_.Exception.Response) {
            Write-Host "HTTP status: $($_.Exception.Response.StatusCode.value__)"
        }

        Write-Host $_.Exception.Message
    }

    Write-Host ""
    Write-Host "------------------------------------------------------------"
}