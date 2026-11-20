$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$serverStatePath = Join-Path $env:LOCALAPPDATA 'Agastya\EYE\server.json'

if (-not (Test-Path -LiteralPath $serverStatePath -PathType Leaf)) {
    throw "No launcher-managed EYE server is recorded. If you started app.py directly, stop it with Ctrl+C in that PowerShell window."
}

$state = Get-Content -LiteralPath $serverStatePath -Raw | ConvertFrom-Json
$expectedScript = [System.IO.Path]::GetFullPath((Join-Path $root 'app.py'))
if ([System.IO.Path]::GetFullPath([string]$state.app_script) -ne $expectedScript) {
    throw "The recorded server belongs to another EYE checkout; refusing to stop it. State file: $serverStatePath"
}

$processId = [int]$state.process_id
$process = Get-CimInstance -ClassName Win32_Process -Filter "ProcessId = $processId" -ErrorAction SilentlyContinue
if (-not $process) {
    Remove-Item -LiteralPath $serverStatePath -Force
    Write-Host 'The recorded EYE server is already stopped.'
    exit 0
}
if ($process.CommandLine -notlike "*$expectedScript*") {
    throw "Process $processId no longer runs the recorded app.py; refusing to stop it."
}

$url = "http://127.0.0.1:$([int]$state.port)/api/v1/admin/shutdown"
try {
    Invoke-RestMethod -Uri $url -Method Post -ContentType 'application/json' -Body '{}' -TimeoutSec 5 | Out-Null
} catch {
    throw "EYE did not accept a graceful shutdown request. The process was left running. Error: $($_.Exception.Message)"
}

$stopped = $false
for ($attempt = 0; $attempt -lt 50; $attempt++) {
    if (-not (Get-Process -Id $processId -ErrorAction SilentlyContinue)) {
        $stopped = $true
        break
    }
    Start-Sleep -Milliseconds 100
}
if (-not $stopped) {
    throw "EYE accepted the shutdown request but process $processId is still running. No force termination was attempted."
}

Remove-Item -LiteralPath $serverStatePath -Force
Write-Host "Agastya EYE stopped cleanly (PID $processId, port $($state.port))."
