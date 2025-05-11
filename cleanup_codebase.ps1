# Cleanup Script for MLSecOps Project
# This script removes redundant and unnecessary files from the codebase

# Set WorkingDirectory
$workingDir = $PSScriptRoot

Write-Host "Starting cleanup process..." -ForegroundColor Green

# 1. Remove redundant configuration files
Write-Host "Removing redundant configuration files..." -ForegroundColor Yellow
if (Test-Path "$workingDir\airflow.cfg") {
    Remove-Item -Path "$workingDir\airflow.cfg" -Force
    Write-Host "  - Removed root airflow.cfg (duplicate, main config is in config/ folder)" -ForegroundColor Cyan
}

# 2. Remove redundant entrypoint scripts
Write-Host "Removing redundant entrypoint scripts..." -ForegroundColor Yellow
if (Test-Path "$workingDir\docker-entrypoint.sh") {
    Remove-Item -Path "$workingDir\docker-entrypoint.sh" -Force
    Write-Host "  - Removed docker-entrypoint.sh (consolidated in scripts/entrypoint.sh)" -ForegroundColor Cyan
}
if (Test-Path "$workingDir\entrypoint.sh") {
    Remove-Item -Path "$workingDir\entrypoint.sh" -Force
    Write-Host "  - Removed entrypoint.sh (consolidated in scripts/entrypoint.sh)" -ForegroundColor Cyan
}

# 3. Remove redundant update_airflow_config.py
Write-Host "Removing redundant Python scripts..." -ForegroundColor Yellow
if (Test-Path "$workingDir\update_airflow_config.py") {
    Remove-Item -Path "$workingDir\update_airflow_config.py" -Force
    Write-Host "  - Removed root update_airflow_config.py (duplicate of scripts/update_airflow_config.py)" -ForegroundColor Cyan
}

# 4. Remove markdown.md (appears to be malformed notebook)
Write-Host "Removing unnecessary documentation files..." -ForegroundColor Yellow
if (Test-Path "$workingDir\markdown.md") {
    Remove-Item -Path "$workingDir\markdown.md" -Force
    Write-Host "  - Removed markdown.md (malformed notebook format)" -ForegroundColor Cyan
}

# 5. Clean up MLflow experiment runs 
# Note: We leave the 3 most recent experiment runs and clean up the rest
Write-Host "Cleaning up old MLflow experiment runs..." -ForegroundColor Yellow
$mlrunsDir = "$workingDir\mlruns"
if (Test-Path $mlrunsDir) {
    # Get all experiment runs sorted by last write time (newest first)
    $dirs = Get-ChildItem -Path "$mlrunsDir\0\*" -Directory | Sort-Object LastWriteTime -Descending
    
    # Get the total number of experiment runs
    $totalRuns = $dirs.Count
    Write-Host "  - Found $totalRuns experiment runs" -ForegroundColor Cyan
    
    # Keep the 3 most recent runs and clean up the rest
    if ($totalRuns -gt 3) {
        $dirsToRemove = $dirs | Select-Object -Skip 3
        
        foreach ($dir in $dirsToRemove) {
            Remove-Item -Path $dir.FullName -Recurse -Force
            Write-Host "  - Removed old MLflow experiment run: $($dir.Name)" -ForegroundColor Cyan
        }
        
        Write-Host "  - Kept 3 most recent experiment runs, removed $($dirsToRemove.Count) old runs" -ForegroundColor Green
    } else {
        Write-Host "  - Only $totalRuns experiment runs found, no cleanup needed" -ForegroundColor Cyan
    }
}

# 6. Clean up any __pycache__ directories
Write-Host "Cleaning up Python cache files..." -ForegroundColor Yellow
$pycacheDirs = Get-ChildItem -Path $workingDir -Recurse -Directory -Filter "__pycache__"
foreach ($dir in $pycacheDirs) {
    Remove-Item -Path $dir.FullName -Recurse -Force
    Write-Host "  - Removed Python cache directory: $($dir.FullName)" -ForegroundColor Cyan
}

# 7. Remove .pyc files
$pycFiles = Get-ChildItem -Path $workingDir -Recurse -File -Filter "*.pyc"
foreach ($file in $pycFiles) {
    Remove-Item -Path $file.FullName -Force
    Write-Host "  - Removed Python compiled file: $($file.FullName)" -ForegroundColor Cyan
}

# 8. Check for consistent docker-compose configuration
Write-Host "Verifying Docker configuration consistency..." -ForegroundColor Yellow

# Check if docker-compose.override.yml service names match docker-compose.yml
$composeFile = "$workingDir\docker-compose.yml"
$overrideFile = "$workingDir\docker-compose.override.yml"

if ((Test-Path $composeFile) -and (Test-Path $overrideFile)) {
    $composeContent = Get-Content $composeFile -Raw
    $overrideContent = Get-Content $overrideFile -Raw
    
    # Get service names from both files
    $composeMatches = [regex]::Matches($composeContent, '(\w[\w\-]+):\s*\n')
    $overrideMatches = [regex]::Matches($overrideContent, '(\w[\w\-]+):\s*\n')
    
    $composeServices = @()
    $overrideServices = @()
    
    foreach ($match in $composeMatches) {
        $composeServices += $match.Groups[1].Value
    }
    
    foreach ($match in $overrideMatches) {
        $overrideServices += $match.Groups[1].Value
    }
    
    # Check for mismatches
    $mismatchFound = $false
    foreach ($service in $overrideServices) {
        if ($composeServices -notcontains $service) {
            $mismatchFound = $true
            Write-Host "  - Warning: Service '$service' in docker-compose.override.yml doesn't match any service in docker-compose.yml" -ForegroundColor Yellow
        }
    }
    
    if (-not $mismatchFound) {
        Write-Host "  - Docker Compose service names are consistent" -ForegroundColor Green
    }
}

# 9. Add a .gitignore entry for MLflow if it doesn't exist
$gitignoreFile = "$workingDir\.gitignore"
if (Test-Path $gitignoreFile) {
    $gitignoreContent = Get-Content $gitignoreFile -Raw
    
    if ($gitignoreContent -notmatch "mlruns/") {
        Write-Host "Adding MLflow runs directory to .gitignore..." -ForegroundColor Yellow
        Add-Content -Path $gitignoreFile -Value "`n# MLflow runs`nmlruns/`n"
        Write-Host "  - Added 'mlruns/' to .gitignore" -ForegroundColor Cyan
    }
}

Write-Host "Cleanup process completed successfully!" -ForegroundColor Green